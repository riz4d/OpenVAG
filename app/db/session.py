from __future__ import annotations

from collections.abc import AsyncGenerator

import aiosqlite

from app.db.base import get_connection


async def get_db() -> AsyncGenerator[aiosqlite.Connection, None]:
    db = await get_connection()
    try:
        yield db
    finally:
        await db.close()
