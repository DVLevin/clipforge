# syntax=docker/dockerfile:1
# =============================================================================
# CLIPFORGE backend - production image.
#
# The FastAPI app lives in the build CONTEXT (= the `backend/` dir): main.py,
# app/, requirements.txt. The image runs the ASGI server on $PORT.
#
# Build (from CLIPFORGE project root):
#   docker build -f deploy/Dockerfile -t clipforge:latest backend/
#   # for cloud (Railway/Render run x86_64):
#   docker build --platform linux/amd64 -f deploy/Dockerfile -t clipforge:latest backend/
#
# Run:
#   docker run --rm -p 8000:8000 --env-file deploy/.env.example clipforge:latest
#   curl localhost:8000/health
# =============================================================================
FROM python:3.11-slim AS runtime

# --- system libs needed by Pillow + onnxruntime + torch + opencv ---
# libgl1 / libglib2.0-0 : Pillow + opencv image codecs
# libgomp1              : OpenMP (onnxruntime / openblas)
# libjpeg / zlib        : fast image decode
RUN apt-get update && apt-get install -y --no-install-recommends \
        libgl1 libglib2.0-0 libgomp1 libjpeg62-turbo zlib1g \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    U2NET_HOME=/data/models

WORKDIR /app

# -----------------------------------------------------------------------------
# Dependency install (ordered to dodge two known pip resolution traps).
#
# Trap 1 - Pillow conflict: rembg pulls Pillow>=12.1 but every
#   simple-lama-inpainting caps Pillow below 11 -> ResolutionImpossible.
#   Fix: install the core requirements WITHOUT simple-lama-inpainting, then add
#   it with --no-deps (its pin is over-cautious; it runs fine on Pillow 12).
#
# Trap 2 - CUDA torch bloat: requirements.txt lists torch>=2.1. On x86_64 the
#   default wheel is the multi-GB CUDA build. Fix: install CPU torch + torchvision
#   FIRST (small), so when the core requirements are installed their torch pins
#   are already satisfied and pip does not pull the CUDA wheels.
# -----------------------------------------------------------------------------
COPY requirements.txt ./

# 1) CPU torch + torchvision first (x86_64 -> CPU index; elsewhere -> default).
RUN if [ "$(uname -m)" = "x86_64" ]; then \
        pip install --no-cache-dir torch torchvision \
            --index-url https://download.pytorch.org/whl/cpu ; \
    else \
        pip install --no-cache-dir torch torchvision ; \
    fi

# 2) core requirements, minus simple-lama-inpainting (which conflicts on Pillow).
RUN grep -v 'simple-lama-inpainting' requirements.txt > /tmp/reqs_core.txt \
    && pip install --no-cache-dir -r /tmp/reqs_core.txt

# 3) simple-lama-inpainting without its conflicting Pillow pin.
RUN pip install --no-cache-dir --no-deps simple-lama-inpainting

# --- app code + web frontend ---
COPY main.py ./
COPY app ./app
COPY static ./static

# --- non-root user + persistent data dir (SQLite db + model cache) ---
RUN useradd --create-home --uid 1000 appuser \
    && mkdir -p /data/models /app/data \
    && chown -R appuser:appuser /data /app
USER appuser

ENV CLIPFORGE_DB_PATH=/data/clipforge.db

EXPOSE 8000

# Liveness/readiness: hit /health (never loads the model -> ~5ms, safe for
# tight probe intervals). Uses stdlib urllib so we don't need curl in the image.
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
    CMD python -c "import os,urllib.request;urllib.request.urlopen('http://127.0.0.1:%s/health' % os.getenv('PORT','8000'), timeout=4).read()" || exit 1

# Railway / Render inject PORT. The ASGI server reads it here.
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000} --proxy-headers --forwarded-allow-ips=*"]
