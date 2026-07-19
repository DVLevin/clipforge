"""Inference layer: lazy-loaded models for background removal + object erasure.

Models (all self-hosted, near-zero marginal cost):
  * Background removal -> rembg (ONNX). Default model isnet-general-use.
  * Object erasure      -> LaMa inpainting (simple-lama-inpainting, PyTorch).

Both models are loaded once on first use and kept in memory for the life of
the process (warm). Cold start downloads ~170MB (isnet) + ~200MB (LaMa).
"""
from __future__ import annotations

import io
import logging
import threading
import time
from typing import Optional

import numpy as np
from PIL import Image

from .config import settings

log = logging.getLogger("clipforge.inference")

# ---------------------------------------------------------------------------
# Background removal (rembg)
# ---------------------------------------------------------------------------
_bg_lock = threading.Lock()
_bg_session = None


def _bg_session_obj():
    """Lazily build a rembg session bound to the configured model."""
    global _bg_session
    if _bg_session is None:
        with _bg_lock:
            if _bg_session is None:
                from rembg import new_session

                log.info("loading rembg model=%s (first call downloads weights)...", settings.bg_model)
                t0 = time.time()
                _bg_session = new_session(settings.bg_model)
                log.info("rembg model ready in %.1fs", time.time() - t0)
    return _bg_session


def remove_background(image_bytes: bytes) -> tuple[bytes, dict]:
    """Run background removal. Returns (png_rgba_bytes, meta)."""
    from rembg import remove

    session = _bg_session_obj()
    t0 = time.time()
    out = remove(
        image_bytes,
        session=session,
        alpha_matting=settings.alpha_matting,
        # sensible caps; rembg resizes internally before inference
        alpha_matting_foreground_threshold=240,
        alpha_matting_background_threshold=10,
        alpha_matting_erode_size=10,
    )
    ms = int((time.time() - t0) * 1000)
    # verify it's RGBA
    img = Image.open(io.BytesIO(out))
    meta = {
        "model": settings.bg_model,
        "mode": img.mode,
        "size": img.size,
        "ms": ms,
    }
    return out, meta


# ---------------------------------------------------------------------------
# Object erasure (LaMa inpainting)
# ---------------------------------------------------------------------------
_lama_lock = threading.Lock()
_lama = None


def _lama_model():
    global _lama
    if _lama is None:
        with _lama_lock:
            if _lama is None:
                import simple_lama_inpainting

                log.info("loading LaMa inpainting model (first call downloads weights)...")
                t0 = time.time()
                _lama = simple_lama_inpainting.SimpleLama()
                log.info("LaMa model ready in %.1fs", time.time() - t0)
    return _lama


def _to_mask_image(mask_bytes: bytes, target_size: tuple[int, int]) -> Image.Image:
    """Normalize an uploaded mask: grayscale, resized to target, binarized.
    Non-black pixels => area to erase."""
    mask = Image.open(io.BytesIO(mask_bytes)).convert("L")
    if mask.size != target_size:
        mask = mask.resize(target_size, Image.BILINEAR)
    arr = np.array(mask)
    # anything brighter than 32/255 counts as "erase here"
    binarized = np.where(arr > 32, 255, 0).astype(np.uint8)
    return Image.fromarray(binarized, mode="L")


def mask_from_bbox(image_size: tuple[int, int], bbox: tuple[int, int, int, int]) -> Image.Image:
    """Build a binary mask covering a bounding box (x1,y1,x2,y2)."""
    w, h = image_size
    x1, y1, x2, y2 = bbox
    arr = np.zeros((h, w), dtype=np.uint8)
    arr[max(0, y1):min(h, y2), max(0, x1):min(w, x2)] = 255
    return Image.fromarray(arr, mode="L")


def erase_objects(
    image_bytes: bytes,
    *,
    mask_bytes: Optional[bytes] = None,
    bbox: Optional[tuple[int, int, int, int]] = None,
) -> tuple[bytes, dict]:
    """Erase objects. Provide either an explicit mask OR a bounding box.
    Returns (png_rgb_bytes, meta)."""
    if mask_bytes is None and bbox is None:
        raise ValueError("erase_objects requires either mask_bytes or bbox")

    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    if bbox is not None:
        mask = mask_from_bbox(img.size, bbox)
    else:
        mask = _to_mask_image(mask_bytes, img.size)

    lama = _lama_model()
    t0 = time.time()
    result = lama(img, mask)  # SimpleLama.__call__(image, mask) -> PIL RGB
    ms = int((time.time() - t0) * 1000)

    buf = io.BytesIO()
    result.save(buf, format="PNG", optimize=True)
    out = buf.getvalue()

    coverage = float((np.array(mask) > 0).mean())
    meta = {
        "model": "lama",
        "size": result.size,
        "mask_coverage_pct": round(coverage * 100, 2),
        "ms": ms,
    }
    return out, meta


# ---------------------------------------------------------------------------
# image sanity helpers
# ---------------------------------------------------------------------------
def validate_and_read(image_bytes: bytes) -> Image.Image:
    img = Image.open(io.BytesIO(image_bytes))
    img.load()
    if img.mode not in ("RGB", "RGBA", "L", "P"):
        img = img.convert("RGB")
    # downscale if huge (keeps latency bounded on free tier)
    edge = max(img.size)
    if edge > settings.max_image_edge:
        scale = settings.max_image_edge / edge
        img = img.resize(
            (int(img.size[0] * scale), int(img.size[1] * scale)), Image.LANCZOS
        )
    return img


def to_png_bytes(img: Image.Image) -> bytes:
    buf = io.BytesIO()
    img.save(buf, format="PNG", optimize=True)
    return buf.getvalue()
