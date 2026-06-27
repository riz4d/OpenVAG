from __future__ import annotations

import aiosqlite

from app.core.config import settings


async def get_connection() -> aiosqlite.Connection:
    db = await aiosqlite.connect(settings.DATABASE_URL)
    db.row_factory = aiosqlite.Row
    await db.execute("PRAGMA journal_mode=WAL")
    await db.execute("PRAGMA foreign_keys=ON")
    return db
