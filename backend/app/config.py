"""Runtime configuration for CLIPFORGE backend.

Reads environment variables (12-factor). A module-level `settings` instance is
imported everywhere: `from app.config import settings`.

NOTE (CLIPFORGE Sprint 5 / deploy): this file was missing when the Sprint 2
backend modules (main.py, inference.py, usage.py, ratelimit.py) were written,
so they could not be imported. This config implements the exact `settings`
contract those modules require. If Sprint 2 ships its own config.py, that is
the source of truth -- just keep these attribute names.
"""
from __future__ import annotations

import os


class _Settings:
    # --- identity ---
    app_name: str = "CLIPFORGE"
    version: str = "0.1.0"

    # --- model selection / behaviour ---
    # rembg model. isnet-general-use = best general quality; alternatives:
    # u2net, u2netp, silueta, birenet-general. See rembg docs.
    bg_model: str = os.getenv("CLIPFORGE_BG_MODEL", "isnet-general-use")
    alpha_matting: bool = os.getenv("CLIPFORGE_ALPHA_MATTING", "false").lower() == "true"
    # downscale huge uploads before inference (longest edge, px)
    max_image_edge: int = int(os.getenv("CLIPFORGE_MAX_IMAGE_EDGE", "1600"))

    # --- limits ---
    max_upload_mb: int = int(os.getenv("MAX_UPLOAD_MB", "15"))
    ratelimit_per_minute: int = int(os.getenv("RATE_LIMIT_PER_MINUTE", "20"))
    free_daily_limit: int = int(os.getenv("FREE_DAILY_LIMIT", "5"))

    # --- auth ---
    # admin key gates POST /admin/keys. Empty = endpoint disabled in practice.
    admin_key: str = os.getenv("CLIPFORGE_ADMIN_KEY", "")

    # --- storage ---
    # SQLite path for usage tracking. Use a persistent volume in prod.
    db_path: str = os.getenv("CLIPFORGE_DB_PATH", "data/clipforge.db")


settings = _Settings()
