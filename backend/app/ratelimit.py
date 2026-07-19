"""slowapi limiter keyed by api-key-or-ip."""
from __future__ import annotations

from slowapi import Limiter
from slowapi.util import get_remote_address

from .config import settings


def _key_func(request) -> str:
    # prefer api key, fall back to ip
    api_key = request.headers.get("X-API-Key")
    if api_key:
        return f"key:{api_key}"
    return f"ip:{get_remote_address(request)}"


limiter = Limiter(key_func=_key_func, default_limits=[])
