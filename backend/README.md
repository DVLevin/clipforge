# CLIPFORGE Backend API

Self-hosted **AI Background Remover + Object Eraser** built on FastAPI.

## Stack (all self-hosted -> ~$0 marginal cost per use)
- **Background removal** -> `rembg` (ONNX). Default model `isnet-general-use`.
- **Object erasure** -> LaMa inpainting via `simple-lama-inpainting` (PyTorch).
- **API** -> FastAPI + Uvicorn.
- **Rate limiting** -> slowapi (per-minute window).
- **Usage tracking + free tier** -> SQLite (`data/usage.db`).

## Quick start
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
# Note: simple-lama-inpainting pins Pillow<10 conservatively. If it conflicts
# with rembg, install it with: pip install --no-deps simple-lama-inpainting==0.1.2
cp .env.template .env   # edit as needed
uvicorn main:app --host 0.0.0.0 --port 8000
```
First call downloads model weights (~170MB isnet + ~200MB LaMa); subsequent calls are fast.

## Endpoints
| Method | Path | Purpose |
|--------|------|---------|
| GET  | `/` | service info |
| GET  | `/health` | health + model load state |
| GET  | `/v1/usage` | caller quota / usage |
| POST | `/v1/remove-background` | cut subject from background -> PNG (RGBA) |
| POST | `/v1/erase-objects` | LaMa inpaint (mask OR bbox) -> PNG (RGB) |
| POST | `/admin/keys` | provision an API key (needs CLIPFORGE_ADMIN_KEY) |

## Auth and free tier
- Optional `X-API-Key` header. Without it, identity falls back to a hash of the client IP.
- Free tier default: **5 successful inferences / identity / UTC day** (`CLIPFORGE_FREE_DAILY_LIMIT`).
- Short-window protection: **20 req/min** (`CLIPFORGE_RPM_LIMIT`).
- Over-quota returns `429` with a `Retry-After` header.

### Examples
```bash
# remove background
curl -F image=@photo.jpg http://localhost:8000/v1/remove-background -o nobg.png

# erase a bounding box (x1,y1,x2,y2)
curl -F image=@photo.jpg -F bbox=100,80,200,180 http://localhost:8000/v1/erase-objects -o erased.png

# erase via a mask file (white = erase)
curl -F image=@photo.jpg -F mask=@mask.png http://localhost:8000/v1/erase-objects -o erased.png
```

## Tests
```bash
.venv/bin/python run_tests.py
```
Produces real outputs in `test_output/` and prints quota status.

## Layout
```
backend/
|-- main.py              FastAPI app + endpoints
|-- run_tests.py         end-to-end test harness
|-- requirements.txt
|-- .env.template
|-- app/
|   |-- config.py        env-driven settings
|   |-- inference.py     rembg + LaMa (lazy-loaded)
|   |-- ratelimit.py     slowapi limiter
|   `-- usage.py         SQLite usage tracking + free tier
|-- data/                usage.db (gitignored)
|-- samples/             test input images (gitignored)
`-- test_output/         sample results proving it works
```
