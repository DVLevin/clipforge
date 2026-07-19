"""End-to-end test harness for the CLIPFORGE backend.

Hits both core endpoints with a real sample image and saves outputs to
test_output/. Run while the API is up: `.venv/bin/python run_tests.py`
"""
from __future__ import annotations

import io
import os
import sys
from pathlib import Path

import httpx
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "test_output"
SAMPLES = ROOT / "samples"
BASE = os.environ.get("CLIPFORGE_TEST_BASE", "http://127.0.0.1:8000")


def make_sample_image(path: Path):
    img = Image.new("RGB", (640, 480), (40, 120, 200))
    d = ImageDraw.Draw(img)
    d.ellipse((210, 130, 430, 380), fill=(220, 40, 40))
    gx1, gy1, gx2, gy2 = 470, 60, 560, 150
    d.rectangle((gx1, gy1, gx2, gy2), fill=(40, 200, 60))
    for y in range(0, 480, 40):
        d.line([(0, y), (640, y)], fill=(60, 140, 220))
    img.save(path, format="PNG")
    return (gx1, gy1, gx2, gy2)


def make_mask(size, bbox):
    w, h = size
    m = Image.new("L", (w, h), 0)
    ImageDraw.Draw(m).rectangle(bbox, fill=255)
    buf = io.BytesIO()
    m.save(buf, format="PNG")
    return buf.getvalue()


def main() -> int:
    OUT.mkdir(exist_ok=True)
    SAMPLES.mkdir(exist_ok=True)
    sample = SAMPLES / "sample_subject.png"
    bbox = make_sample_image(sample)
    print(f"[test] sample -> {sample}  bbox={bbox}")

    with open(sample, "rb") as f:
        img_bytes = f.read()

    # 1. remove background
    print("[test] POST /v1/remove-background")
    r = httpx.post(f"{BASE}/v1/remove-background",
                   files={"image": ("sample.png", img_bytes, "image/png")}, timeout=300)
    print(f"[test]   status={r.status_code} ms={r.headers.get('X-Ms')} model={r.headers.get('X-Model')}")
    if r.status_code != 200:
        print("[test]   FAIL:", r.text[:500]); return 1
    (OUT / "bg_removed.png").write_bytes(r.content)
    im = Image.open(io.BytesIO(r.content))
    print(f"[test]   saved bg_removed.png mode={im.mode} size={im.size}")

    # 2. erase objects (bbox)
    print(f"[test] POST /v1/erase-objects bbox={bbox}")
    r = httpx.post(f"{BASE}/v1/erase-objects",
                   files={"image": ("sample.png", img_bytes, "image/png")},
                   data={"bbox": f"{bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]}"}, timeout=300)
    print(f"[test]   status={r.status_code} ms={r.headers.get('X-Ms')} coverage={r.headers.get('X-Mask-Coverage-Pct')}")
    if r.status_code != 200:
        print("[test]   FAIL:", r.text[:500]); return 1
    (OUT / "object_erased_bbox.png").write_bytes(r.content)
    print("[test]   saved object_erased_bbox.png")

    # 3. erase objects (mask)
    mask_bytes = make_mask((640, 480), bbox)
    (OUT / "mask_used.png").write_bytes(mask_bytes)
    print("[test] POST /v1/erase-objects (mask)")
    r = httpx.post(f"{BASE}/v1/erase-objects",
                   files={"image": ("sample.png", img_bytes, "image/png"),
                          "mask": ("mask.png", mask_bytes, "image/png")}, timeout=300)
    print(f"[test]   status={r.status_code} ms={r.headers.get('X-Ms')}")
    if r.status_code != 200:
        print("[test]   FAIL:", r.text[:500]); return 1
    (OUT / "object_erased_mask.png").write_bytes(r.content)
    print("[test]   saved object_erased_mask.png")

    # 4. usage
    r = httpx.get(f"{BASE}/v1/usage", timeout=30)
    print(f"[test] GET /v1/usage -> {r.json()}")
    print("\n[test] ALL CORE TESTS PASSED.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
