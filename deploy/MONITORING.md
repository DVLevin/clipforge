# CLIPFORGE - First 24 Hours Monitoring Checklist

> Run this after the first production deploy (Railway or Render). Goal: catch
> the failure modes that bite ML-backed APIs in the first day - cold model
> loads, OOM, weight re-downloads, and silent quota drift.

The service is healthy when `/health` returns 200 with `bg_loaded`/`lama_loaded`
turning `true` after their first real request. Assume the deploy URL is in
`$BASE` and the admin key is in `$ADMIN`:

```bash
export BASE=https://clipforge-production.up.railway.app   # or your onrender URL
export ADMIN=your-CLIPFORGE_ADMIN_KEY
```

---

## Hour 0 - deploy smoke test (5 min)

- [ ] `curl -s $BASE/health` returns 200 and JSON with `"status":"ok"`.
- [ ] `curl -s $BASE/` lists the four endpoints.
- [ ] `curl -s $BASE/v1/usage` returns a `free` quota object (identity is a hash
      of your IP). `remaining` should equal `daily_limit`.
- [ ] **Warm the models** (do this once, so the first real user does not pay the
      cold-start wait):
      ```bash
      curl -s -X POST $BASE/v1/remove-background -F "image=@test.jpg" -o /tmp/nobg.png
      curl -s $BASE/health     # bg_loaded should now be true
      ```
      First call downloads ~170 MB isnet weights (15-40 s). Confirm `/tmp/nobg.png`
      opens and has an alpha channel.
- [ ] (optional) warm LaMa similarly via `/v1/erase-objects` with a small mask.

If `/health` is 200 but the first `/v1/remove-background` 502s, check logs for
"rembg model ready" - the download may still be in progress.

---

## Hours 1-6 - stability watch

- [ ] **No restart loops.** Railway: Service > Deployments - the healthcheck
      should be "passing". Render: "Events" tab - look for "instance restarted".
- [ ] **Memory under cap.** dashboard > Metrics > Memory. After both models load
      resident RAM is ~600 MB-1.2 GB. If it kisses the plan limit and the
      container restarts -> bump RAM (LaMa is the hog).
- [ ] **CPU spikes are bounded.** Each inference is a short CPU spike (1-5 s).
      Sustained 100% CPU with no traffic = stuck request; restart the instance.
- [ ] **Disk stable.** `/data` holds the SQLite db + model cache (~370 MB
      weights). If disk grows past ~1 GB without explainable cause, inspect the
      usage table (see Hour 24).

Catch logs in one place:

```bash
railway logs               # Railway CLI
render logs --service clipforge   # Render CLI
```

---

## Hours 6-24 - correctness + quota

- [ ] **Latency sanity.** Hit the endpoint a few times; the `X-Ms` response
      header reports inference ms. Expect: bg removal 500-3000 ms; erase
      1000-6000 ms. Persistently > 10 s = investigate.
- [ ] **429 rate-limit rate.** Grep logs for `429`. A few is normal. A flood
      means `RATE_LIMIT_PER_MINUTE` is too low - raise it.
- [ ] **Quota math holds.** Inspect today's usage directly:
      ```bash
      sqlite3 /data/clipforge.db \
        "SELECT endpoint, COUNT(*) FROM usage WHERE success=1 \
         AND substr(created_at,1,10)=date('now') GROUP BY endpoint;"
      ```
      Compare with what `/v1/usage` reports for a known identity. If free users
      exceed `FREE_DAILY_LIMIT`, `enforce_quota` is wrong.
- [ ] **5xx count = ~0.** Any 502 ("background removal failed") that is not the
      first-call weight download is a real bug - capture the input image.
- [ ] **Weights did not re-download.** After a redeploy, the first request
      should NOT take 30 s. If it does, `U2NET_HOME`/`/data` is not persistent.

---

## Alerts to set up (do this in Hour 0)

| Signal | Threshold | Where | Action |
|---|---|---|---|
| Deploy health | `/health` non-200 for 60 s | Railway/Render built-in | page on-call |
| Restart count | > 3 restarts / 10 min | metrics / events | check OOM, bump RAM |
| Memory | > 90% of plan for 5 min | dashboard metrics | bump plan |
| 5xx rate | > 1% of requests / 5 min | add APM later (Sentry) | investigate inputs |
| Disk | /data > 80% | dashboard | prune old usage rows |

For richer error tracking, set `SENTRY_DSN` (the config reads it) once a Sentry
project exists - wire it into `main.py` in a follow-up.

---

## Known first-day failure modes (and the fix)

1. **First request 502s then succeeds.** Cause: weights still downloading on the
   first call. Fix: pre-warm during Hour 0, or set a longer healthcheck grace.
2. **Container OOM-killed on first LaMa call.** Cause: < 1 GB RAM. Fix: bump the
   plan; LaMa + torch resident is ~700 MB alone.
3. **Quota resets on every deploy.** Cause: `CLIPFORGE_DB_PATH` not persisted.
   Fix: mount `/data` as a volume.
4. **Every deploy re-downloads 370 MB.** Cause: `U2NET_HOME` not persisted. Fix:
   keep `/data/models` on the same volume.
5. **`/health` flaps after deploy.** Cause: a cold model load blocking the event
   loop. `/health` never loads models, so this means something else blocked the
   loop - check for a sync call on the hot path.

---

## Rollback (if something is broken)

- **Railway:** dashboard > Deployments > "Redeploy" the last known-good commit.
- **Render:** dashboard > Manual Deploy > pick the previous commit.
- The `/data` volume survives rollbacks, so quota state + cached weights persist.

---

## End-of-day-1 sign-off

- [ ] `/health` 200, both models `*_loaded: true`.
- [ ] Zero unexpected restarts in the last 6 hours.
- [ ] Memory headroom > 15%.
- [ ] At least one real end-to-end `/v1/remove-background` verified by eye.
- [ ] Quota table matches `/v1/usage` for a test identity.
- [ ] Persistent volume confirmed (weights did not re-download after a redeploy).

If all six pass, the backend is production-stable. Hand off to the mobile-app
session for client integration.
