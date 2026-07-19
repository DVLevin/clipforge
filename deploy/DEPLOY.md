# CLIPFORGE - Deployment Guide

> **Scope (Sprint 5, FACT-24):** deploy the **backend** (FastAPI API server:
> `/health`, `/v1/remove-background`, `/v1/erase-objects`, `/v1/usage`,
> `/admin/keys`). The Android app build is a separate session with Dima.

The backend is a self-hosted AI Background Remover + Object Eraser:

- **Background removal** -> `rembg` (ONNX, model `isnet-general-use`, ~170 MB
  weights, downloaded once on first use).
- **Object erasure** -> `simple-lama-inpainting` (LaMa, ~200 MB weights).
- **Usage/quota** -> SQLite at `$CLIPFORGE_DB_PATH` (free tier =
  `$FREE_DAILY_LIMIT` successful calls / UTC day, per API key or hashed IP).
- **Rate limiting** -> `slowapi` (`$RATE_LIMIT_PER_MINUTE` / min per identity).

Unit cost is ~$0 (self-hosted models) - the only cost is container RAM/CPU.

---

## 0. Prerequisites

- Docker 24+ (to build/test locally).
- Backend code present at `backend/` (`main.py`, `app/`, `requirements.txt`).
- (Optional) accounts on **Railway** or **Render**.

> **Note on a missing file:** the Sprint 2 backend imports
> `from app.config import settings`. If `backend/app/config.py` is missing the
> app will not boot. A contract-faithful `config.py` ships in this repo (its
> env-var names are listed in `.env.example`). If Sprint 2 ships its own, keep
> the attribute names.

> **Known dependency conflict (fixed in the Dockerfile):** rembg>=2.0.50 pulls
> Pillow>=12.1, but every `simple-lama-inpainting` version caps Pillow below 11.
> pip cannot resolve them together, so the Dockerfile installs the core deps
> (without lama), then torch, then `simple-lama-inpainting --no-deps`. See the
> comments in `deploy/Dockerfile`.

---

## 1. Build and verify locally (Docker)

From the **CLIPFORGE project root** (`apps/CLIPFORGE/`):

```bash
# native arch (fastest on your machine)
docker build -f deploy/Dockerfile -t clipforge:latest backend/

# OR a full local stack via compose (recommended):
cp deploy/.env.example deploy/.env        # then edit CLIPFORGE_ADMIN_KEY
docker compose -f deploy/docker-compose.yml up --build
```

Smoke test (verified working during Sprint 5):

```bash
docker run --rm -d -p 8000:8000 --name clipforge clipforge:latest
sleep 6
docker ps --filter name=clipforge --format "{{.Status}}"   # -> Up ... (healthy)
curl -s localhost:8000/health
# {"status":"ok","bg_model":"isnet-general-use","bg_loaded":false,"lama_loaded":false,"free_daily_limit":5}

# background removal (first call downloads ~170 MB isnet weights, then caches):
curl -s -X POST localhost:8000/v1/remove-background -F "image=@some-photo.jpg" -o nobg.png
file nobg.png                              # PNG with an alpha channel

docker stop clipforge
```

`/health` never loads the model, so it answers in ~5 ms - ideal for platform
health probes. The image is large (~2-3 GB on amd64, ~5.8 GB on arm64) because
of torch + onnxruntime. Production builds use the CPU torch wheel (smaller).

---

## 2. Environment variables (production)

See `deploy/.env.example`. Minimum to set in the cloud dashboard:

| Variable | Example | Why |
|---|---|---|
| `PORT` | `8000` | Railway/Render inject this. The container reads `$PORT`. |
| `CLIPFORGE_ENV` | `production` | Marks the deployment. |
| `CLIPFORGE_BG_MODEL` | `isnet-general-use` | rembg model. |
| `MAX_UPLOAD_MB` | `15` | Reject oversize uploads (413). |
| `RATE_LIMIT_PER_MINUTE` | `20` | Per-identity slowapi limit. |
| `FREE_DAILY_LIMIT` | `5` | Free-tier daily quota. |
| `CLIPFORGE_ADMIN_KEY` | `long-random-string` | Gates `POST /admin/keys`. **Set this.** |
| `CLIPFORGE_DB_PATH` | `/data/clipforge.db` | SQLite path - point at a **persistent volume**. |
| `U2NET_HOME` | `/data/models` | rembg weights cache - keep on a volume. |

**Critical:** the SQLite db (`CLIPFORGE_DB_PATH`) and the model cache
(`U2NET_HOME`) **must live on a persistent volume**, or every restart loses
quota state and re-downloads ~370 MB of weights.

---

## 3. Deploy to Railway

Railway builds the Dockerfile and runs it. Plan: **Hobby ($5/mo)** minimum -
LaMa needs ~1 GB RAM.

```bash
brew install railway          # one-time
railway login
railway init                  # create project "clipforge"
railway up                    # deploys deploy/Dockerfile (auto-detected)
```

If Railway picks the wrong root, set Service > Settings > Root Directory to the
folder whose `backend/` is the Docker build context.

Configure variables (one per line):

```bash
railway variables set CLIPFORGE_ENV=production
railway variables set CLIPFORGE_ADMIN_KEY=$(openssl rand -hex 24)
railway variables set FREE_DAILY_LIMIT=5
railway variables set RATE_LIMIT_PER_MINUTE=20
railway variables set MAX_UPLOAD_MB=15
railway variables set CLIPFORGE_DB_PATH=/data/clipforge.db
railway variables set U2NET_HOME=/data/models
```

- **Persistent volume:** Service > Settings > Volumes > add a volume mounted at
  `/data` (covers the SQLite db + model cache).
- **Healthcheck:** Service > Settings > Healthcheck > Path `/health` (Railway
  also reads the Dockerfile `HEALTHCHECK`).
- **Domain:** Settings > Networking > Generate Domain ->
  `clipforge-production.up.railway.app`.
- **Plan:** >= 1 GB RAM (Settings > Resources). The first cold request to each
  endpoint downloads + loads weights (~15-40 s one-time).

Smoke test:

```bash
curl -s https://clipforge-production.up.railway.app/health
```

Re-deploy on every push: `railway up` (or connect a GitHub repo for auto-deploy).

---

## 4. Deploy to Render

Use a **Web Service** from the Dockerfile.

```bash
brew tap render-oss/render     # one-time
brew install render
render login
```

Dashboard path (recommended):

1. **New > Web Service > Docker** -> connect repo -> pick the folder with
   `deploy/Dockerfile`. Set:
   - **Dockerfile Path:** `deploy/Dockerfile` (if Render asks).
   - **Docker Build Context Directory:** `backend` (where `main.py` lives).
2. **Instance type:** >= 1 GB RAM. LaMa needs it.
3. **Environment variables:** paste the table from section 2.
4. **Disk:** add a persistent **Disk** mounted at `/data` (5 GB is plenty).
5. **Health Check:** set **Health Check Path** = `/health`.
6. Deploy -> wait for "Live". Grab the `onrender.com` URL.

```bash
curl -s https://clipforge-xxxx.onrender.com/health
```

For IaC, a minimal `render.yaml` at the repo root:

```yaml
services:
  - type: web
    name: clipforge
    env: docker
    dockerfilePath: ./deploy/Dockerfile
    dockerContext: ./backend
    healthCheckPath: /health
    plan: starter
    disk:
      name: clipforge-data
      mountPath: /data
      sizeGB: 5
    envVars:
      - key: CLIPFORGE_ENV
        value: production
      - key: CLIPFORGE_ADMIN_KEY
        sync: false            # set in dashboard (secret)
      - key: CLIPFORGE_DB_PATH
        value: /data/clipforge.db
      - key: U2NET_HOME
        value: /data/models
      - key: FREE_DAILY_LIMIT
        value: "5"
      - key: RATE_LIMIT_PER_MINUTE
        value: "20"
      - key: MAX_UPLOAD_MB
        value: "15"
```

Apply with `render blueprint apply` (after pushing `render.yaml`).

---

## 5. Provision a paying key (after deploy)

```bash
ADMIN=your-CLIPFORGE_ADMIN_KEY
BASE=https://clipforge-production.up.railway.app   # or your onrender URL

curl -s -X POST "$BASE/admin/keys" -H "X-API-Key: $ADMIN" -H "Content-Type: application/json" -d '{"key":"prod-mobile-app-key","tier":"pro","daily_limit":1000,"note":"android app"}'
```

Clients then send `X-API-Key: prod-mobile-app-key` on every request and are
tracked under the `pro` quota (1000/day here) instead of free.

---

## 6. Updating / rolling back

- **Railway:** `railway up` redeploys. Roll back: dashboard > Deployments >
  Redeploy a previous commit. Volumes persist across redeployments.
- **Render:** push to the branch > auto-deploy. Roll back: dashboard > Manual
  Deploy > Deploy a specific commit.

Both keep the `/data` volume across deploys, so quota state + cached weights
survive.

---

## 7. Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `502 background removal failed` on first call | weights still downloading | wait ~30 s; check logs for "rembg model ready" |
| container OOM-killed / restarts | < 1 GB RAM (LaMa) | bump plan to >= 1 GB |
| `/health` flaps after deploy | model cold load blocks event loop | keep model lazy (default); `/health` never loads models |
| quota resets every restart | `CLIPFORGE_DB_PATH` not on a volume | mount `/data` persistently |
| 429 too many requests | hit `RATE_LIMIT_PER_MINUTE` | raise it, or use a provisioned `pro` key |
| weights re-download each deploy | `U2NET_HOME` not persistent | mount `/data/models` on a volume |
| build fails with ResolutionImpossible | Pillow conflict | the Dockerfile already does the two-phase install; do not bypass it |
