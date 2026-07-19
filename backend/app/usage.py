"""SQLite-backed usage tracking + free-tier enforcement.

Identity model: every request is keyed by an *identity* which is either the
 supplied API key (`X-API-Key` header) or, when absent, a hash of the client IP.
 Free tier = `free_daily_limit` successful inferences per UTC day. Paying keys
 can be provisioned in the `api_keys` table with a custom `daily_limit`.
"""
from __future__ import annotations

import hashlib
import logging
import os
import sqlite3
import threading
import time
from contextlib import contextmanager
from datetime import datetime, timezone
from typing import Optional

from .config import settings

log = logging.getLogger("clipforge.usage")

_lock = threading.Lock()


def _connect() -> sqlite3.Connection:
    os.makedirs(os.path.dirname(settings.db_path), exist_ok=True)
    conn = sqlite3.connect(settings.db_path, timeout=30, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA busy_timeout=5000;")
    return conn


_db = _connect()


def init_db() -> None:
    with _lock, _db:
        _db.executescript(
            """
            CREATE TABLE IF NOT EXISTS usage (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                identity   TEXT NOT NULL,
                endpoint   TEXT NOT NULL,
                model      TEXT,
                success    INTEGER NOT NULL,
                ms_taken   INTEGER,
                bytes_in   INTEGER,
                bytes_out  INTEGER,
                created_at TEXT NOT NULL
            );
            CREATE INDEX IF NOT EXISTS idx_usage_identity_time
                ON usage(identity, created_at);
            CREATE TABLE IF NOT EXISTS api_keys (
                key         TEXT PRIMARY KEY,
                tier        TEXT NOT NULL DEFAULT 'free',   -- free | pro | admin
                daily_limit INTEGER NOT NULL DEFAULT 5,
                created_at  TEXT NOT NULL,
                note        TEXT
            );
            """
        )
    log.info("usage db ready at %s", settings.db_path)


def resolve_identity(api_key: Optional[str], client_ip: Optional[str]) -> tuple[str, str]:
    """Return (identity, tier). Identity = api_key if given, else hashed ip."""
    if api_key:
        tier = _tier_for(api_key)
        return api_key, tier
    ip = client_ip or "unknown"
    digest = hashlib.sha256(f"anon:{ip}".encode()).hexdigest()[:16]
    return digest, "free"


def _tier_for(api_key: str) -> str:
    if settings.admin_key and api_key == settings.admin_key:
        return "admin"
    row = _db.execute("SELECT tier FROM api_keys WHERE key = ?", (api_key,)).fetchone()
    return row["tier"] if row else "free"


def daily_limit_for(tier: str, api_key: Optional[str]) -> int:
    if tier == "admin":
        return 10**9  # effectively unlimited
    if tier in ("pro", "paid"):
        row = None
        if api_key:
            row = _db.execute(
                "SELECT daily_limit FROM api_keys WHERE key = ?", (api_key,)
            ).fetchone()
        return row["daily_limit"] if row else 100
    return settings.free_daily_limit


def today_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def used_today(identity: str) -> int:
    day = today_utc()
    row = _db.execute(
        "SELECT COUNT(*) AS c FROM usage WHERE identity = ? AND success = 1 "
        "AND substr(created_at,1,10) = ?",
        (identity, day),
    ).fetchone()
    return row["c"]


class QuotaExceeded(Exception):
    pass


def check_and_record(
    *,
    identity: str,
    endpoint: str,
    model: Optional[str],
    success: bool,
    ms_taken: int,
    bytes_in: int = 0,
    bytes_out: int = 0,
) -> None:
    """Record a usage row. Caller is responsible for enforcing the quota BEFORE
    running inference via `quota_remaining`."""
    with _lock, _db:
        _db.execute(
            "INSERT INTO usage(identity, endpoint, model, success, ms_taken, "
            "bytes_in, bytes_out, created_at) VALUES (?,?,?,?,?,?,?,?)",
            (
                identity,
                endpoint,
                model,
                1 if success else 0,
                ms_taken,
                bytes_in,
                bytes_out,
                datetime.now(timezone.utc).isoformat(timespec="seconds"),
            ),
        )


def quota_status(identity: str, tier: str, api_key: Optional[str]) -> dict:
    used = used_today(identity)
    limit = daily_limit_for(tier, api_key)
    return {
        "identity": identity,
        "tier": tier,
        "used_today": used,
        "daily_limit": limit,
        "remaining": max(0, limit - used),
        "reset_at": f"{today_utc()}T23:59:59Z",
    }


def provision_key(key: str, tier: str = "pro", daily_limit: int = 100, note: str = "") -> None:
    with _lock, _db:
        _db.execute(
            "INSERT OR REPLACE INTO api_keys(key, tier, daily_limit, created_at, note) "
            "VALUES (?,?,?,?,?)",
            (key, tier, daily_limit, datetime.now(timezone.utc).isoformat(timespec="seconds"), note),
        )
    log.info("provisioned key tier=%s limit=%d note=%s", tier, daily_limit, note)
