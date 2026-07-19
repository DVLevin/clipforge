"""CLIPFORGE API — AI Background Remover + Object Eraser.

Endpoints:
  GET  /                         service info
  GET  /health                   health + model readiness
  GET  /v1/usage                 current quota for the caller
  POST /v1/remove-background     cut subject from background -> PNG (RGBA)
  POST /v1/erase-objects         inpaint/erase objects (mask or bbox) -> PNG (RGB)
  POST /admin/keys               provision an api key (admin only)

Run:
  uvicorn main:app --host 0.0.0.0 --port 8000
"""
from __future__ import annotations

import logging
import os
import time
from typing import Optional

from pathlib import Path as _Path

from fastapi import (
    Depends,
    FastAPI,
    File,
    Form,
    Header,
    HTTPException,
    Request,
    Response,
    UploadFile,
    status,
)
from fastapi.responses import JSONResponse, PlainTextResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from app import inference, usage
from app.config import settings
from app.ratelimit import limiter

# ---------------------------------------------------------------------------
# logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=os.getenv("CLIPFORGE_LOG", "INFO"),
    format="%(asctime)s %(levelname)s %(name)s | %(message)s",
)
log = logging.getLogger("clipforge.main")

# ---------------------------------------------------------------------------
# app
# ---------------------------------------------------------------------------
app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    description="Self-hosted AI Background Remover + Object Eraser.",
)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)


@app.on_event("startup")
def _startup() -> None:
    usage.init_db()


# ---------------------------------------------------------------------------
# identity resolution dependency
# ---------------------------------------------------------------------------
def caller(request: Request, x_api_key: Optional[str] = Header(default=None, alias="X-API-Key")):
    identity, tier = usage.resolve_identity(x_api_key, request.client.host if request.client else None)
    return {"identity": identity, "tier": tier, "api_key": x_api_key, "request": request}


def enforce_quota(c=Depends(caller)) -> dict:
    status_ = usage.quota_status(c["identity"], c["tier"], c["api_key"])
    if status_["remaining"] <= 0:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail={
                "error": "free_tier_limit_reached",
                "message": f"Daily free limit ({status_['daily_limit']}) reached. "
                "Upgrade for more uses.",
                "quota": status_,
            },
            headers={"Retry-After": "3600"},
        )
    c["quota"] = status_
    return c


# ---------------------------------------------------------------------------
# routes: meta
# ---------------------------------------------------------------------------
_STATIC_DIR = _Path(__file__).parent / "static"


@app.get("/")
def root():
    """Serve the CLIPFORGE web app."""
    index = _STATIC_DIR / "index.html"
    if index.exists():
        return FileResponse(str(index))
    return JSONResponse({
        "service": settings.app_name,
        "version": settings.version,
        "note": "Web UI not found. API at /docs",
    })


# Mount static files (CSS, JS, images) if the directory exists
if _STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(_STATIC_DIR)), name="static")


@app.get("/health")
def health():
    return {
        "status": "ok",
        "bg_model": settings.bg_model,
        "bg_loaded": inference._bg_session is not None,
        "lama_loaded": inference._lama is not None,
        "free_daily_limit": settings.free_daily_limit,
    }


@app.get("/v1/usage", dependencies=[Depends(caller)])
def get_usage(c=Depends(caller)):
    return usage.quota_status(c["identity"], c["tier"], c["api_key"])


# ---------------------------------------------------------------------------
# routes: core inference
# ---------------------------------------------------------------------------
def _read_capped(file: UploadFile) -> bytes:
    data = file.file.read(settings.max_upload_mb * 1024 * 1024 + 1)
    if len(data) > settings.max_upload_mb * 1024 * 1024:
        raise HTTPException(
            status_code=413,
            detail=f"Image exceeds max upload size ({settings.max_upload_mb}MB).",
        )
    return data


@app.post("/v1/remove-background")
@limiter.limit(f"{settings.ratelimit_per_minute}/minute")
def remove_background(
    request: Request,
    image: UploadFile = File(...),
    c: dict = Depends(enforce_quota),
):
    """Remove the background from an image. Returns a PNG with transparent
    background (RGBA)."""
    raw = _read_capped(image)
    bytes_in = len(raw)
    t0 = time.time()
    try:
        inference.validate_and_read(raw)  # validate + downscale
        png, meta = inference.remove_background(raw)
    except Exception as e:  # noqa: BLE001
        log.warning("remove_background failed: %s", e)
        usage.check_and_record(
            identity=c["identity"],
            endpoint="/v1/remove-background",
            model=settings.bg_model,
            success=False,
            ms_taken=int((time.time() - t0) * 1000),
            bytes_in=bytes_in,
        )
        raise HTTPException(status_code=422, detail=f"processing_failed: {e}")
    ms_total = int((time.time() - t0) * 1000)
    usage.check_and_record(
        identity=c["identity"],
        endpoint="/v1/remove-background",
        model=settings.bg_model,
        success=True,
        ms_taken=ms_total,
        bytes_in=bytes_in,
        bytes_out=len(png),
    )
    return Response(
        content=png,
        media_type="image/png",
        headers={
            "X-Model": meta["model"],
            "X-Ms": str(meta["ms"]),
            "X-Quota-Remaining": str(c["quota"]["remaining"] - 1),
            "Content-Disposition": 'attachment; filename="clipforge_nobg.png"',
        },
    )


@app.post("/v1/erase-objects")
@limiter.limit(f"{settings.ratelimit_per_minute}/minute")
def erase_objects(
    request: Request,
    image: UploadFile = File(...),
    mask: Optional[UploadFile] = File(default=None),
    bbox: Optional[str] = Form(default=None),
    c: dict = Depends(enforce_quota),
):
    """Erase objects from an image via LaMa inpainting.

    Provide EITHER:
      - `mask`: a grayscale/alpha image (bright pixels = erase)
      - `bbox`: "x1,y1,x2,y2" of a rectangle to erase
    """
    raw = _read_capped(image)
    bytes_in = len(raw)
    mask_bytes = None
    if mask is not None:
        mask_bytes = _read_capped(mask)

    bbox_tuple = None
    if bbox:
        try:
            parts = [int(v.strip()) for v in bbox.split(",")]
            if len(parts) != 4:
                raise ValueError
            bbox_tuple = (parts[0], parts[1], parts[2], parts[3])  # type: ignore
        except ValueError:
            raise HTTPException(status_code=400, detail="bbox must be 'x1,y1,x2,y2' integers")

    if mask_bytes is None and bbox_tuple is None:
        raise HTTPException(
            status_code=400,
            detail="Provide either a `mask` file or a `bbox` form field.",
        )

    t0 = time.time()
    try:
        inference.validate_and_read(raw)
        png, meta = inference.erase_objects(raw, mask_bytes=mask_bytes, bbox=bbox_tuple)
    except Exception as e:  # noqa: BLE001
        log.warning("erase_objects failed: %s", e)
        usage.check_and_record(
            identity=c["identity"],
            endpoint="/v1/erase-objects",
            model="lama",
            success=False,
            ms_taken=int((time.time() - t0) * 1000),
            bytes_in=bytes_in,
        )
        raise HTTPException(status_code=422, detail=f"processing_failed: {e}")
    ms_total = int((time.time() - t0) * 1000)
    usage.check_and_record(
        identity=c["identity"],
        endpoint="/v1/erase-objects",
        model="lama",
        success=True,
        ms_taken=ms_total,
        bytes_in=bytes_in,
        bytes_out=len(png),
    )
    return Response(
        content=png,
        media_type="image/png",
        headers={
            "X-Model": meta["model"],
            "X-Ms": str(meta["ms"]),
            "X-Mask-Coverage-Pct": str(meta["mask_coverage_pct"]),
            "X-Quota-Remaining": str(c["quota"]["remaining"] - 1),
            "Content-Disposition": 'attachment; filename="clipforge_erased.png"',
        },
    )


# ---------------------------------------------------------------------------
# admin
# ---------------------------------------------------------------------------
class KeyRequest(BaseModel):
    key: str = Field(..., min_length=8)
    tier: str = Field("pro")
    daily_limit: int = Field(100)
    note: str = Field("")


@app.post("/admin/keys")
def provision_key(req: KeyRequest, x_api_key: str = Header(..., alias="X-API-Key")):
    if not settings.admin_key or x_api_key != settings.admin_key:
        raise HTTPException(status_code=403, detail="admin key required")
    if req.tier not in ("free", "pro", "admin"):
        raise HTTPException(status_code=400, detail="tier must be free|pro|admin")
    usage.provision_key(req.key, req.tier, req.daily_limit, req.note)
    return {"ok": True, "key": req.key, "tier": req.tier, "daily_limit": req.daily_limit}


@app.exception_handler(429)
async def _429_handler(request: Request, exc: HTTPException):  # noqa: D401
    return JSONResponse(status_code=429, content=exc.detail, headers=exc.headers or {})
