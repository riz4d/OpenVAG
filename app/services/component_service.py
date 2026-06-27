from __future__ import annotations

import aiosqlite

from app.schemas.component import Component, ComponentDetail, ComponentDTCCode


async def get_by_identifier(
    db: aiosqlite.Connection,
    identifier: str,
) -> ComponentDetail | None:
    cursor = await db.execute(
        "SELECT id, identifier, description FROM components WHERE identifier = ?",
        (identifier.upper(),),
    )
    row = await cursor.fetchone()
    if not row:
        return None

    component_id = row["id"]

    cursor = await db.execute(
        "SELECT c.code, c.title FROM dtc_codes c "
        "JOIN dtc_components dc ON dc.dtc_code_id = c.id "
        "WHERE dc.component_id = ? "
        "ORDER BY c.code",
        (component_id,),
    )
    dtc_rows = await cursor.fetchall()
    dtc_codes = [ComponentDTCCode(code=r["code"], title=r["title"]) for r in dtc_rows]

    return ComponentDetail(
        identifier=row["identifier"],
        description=row["description"],
        dtc_codes=dtc_codes,
    )


async def list_components(
    db: aiosqlite.Connection,
    limit: int,
    offset: int,
) -> tuple[list[Component], int]:
    cursor = await db.execute("SELECT COUNT(*) as cnt FROM components")
    row = await cursor.fetchone()
    total = row["cnt"]

    cursor = await db.execute(
        "SELECT identifier, description FROM components ORDER BY identifier LIMIT ? OFFSET ?",
        (limit, offset),
    )
    rows = await cursor.fetchall()
    items = [Component(identifier=r["identifier"], description=r["description"]) for r in rows]

    return items, total
