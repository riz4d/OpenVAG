from __future__ import annotations

import aiosqlite

from app.schemas.dtc import DTCCode, DTCDetail, DTCSearchResult, DTCVariant


def _split_semicolon(value: str | None) -> list[str]:
    if not value:
        return []
    return [item.strip() for item in value.split(";") if item.strip()]


async def get_by_code(db: aiosqlite.Connection, code: str) -> DTCDetail | None:
    cursor = await db.execute(
        "SELECT id, code, title FROM dtc_codes WHERE code = ?",
        (code,),
    )
    row = await cursor.fetchone()
    if not row:
        return None

    dtc_id = row["id"]
    dtc_code = row["code"]
    dtc_title = row["title"]

    cursor = await db.execute(
        "SELECT subtitle, symptoms, causes, solutions, special_notes "
        "FROM dtc_variants WHERE dtc_code_id = ?",
        (dtc_id,),
    )
    variant_rows = await cursor.fetchall()
    variants = [
        DTCVariant(
            subtitle=r["subtitle"],
            symptoms=_split_semicolon(r["symptoms"]),
            causes=_split_semicolon(r["causes"]),
            solutions=_split_semicolon(r["solutions"]),
            special_notes=r["special_notes"],
        )
        for r in variant_rows
    ]

    cursor = await db.execute(
        "SELECT comp.identifier FROM components comp "
        "JOIN dtc_components dc ON dc.component_id = comp.id "
        "WHERE dc.dtc_code_id = ?",
        (dtc_id,),
    )
    component_rows = await cursor.fetchall()
    components = [r["identifier"] for r in component_rows]

    cursor = await db.execute(
        "SELECT related_code FROM related_codes WHERE dtc_code_id = ?",
        (dtc_id,),
    )
    related_rows = await cursor.fetchall()
    related_codes = [r["related_code"] for r in related_rows]

    return DTCDetail(
        code=dtc_code,
        title=dtc_title,
        variants=variants,
        components=components,
        related_codes=related_codes,
    )


async def list_codes(
    db: aiosqlite.Connection,
    limit: int,
    offset: int,
) -> tuple[list[DTCCode], int]:
    cursor = await db.execute("SELECT COUNT(*) as cnt FROM dtc_codes")
    row = await cursor.fetchone()
    total = row["cnt"]

    cursor = await db.execute(
        "SELECT code, title FROM dtc_codes ORDER BY code LIMIT ? OFFSET ?",
        (limit, offset),
    )
    rows = await cursor.fetchall()
    items = [DTCCode(code=r["code"], title=r["title"]) for r in rows]

    return items, total


async def search(
    db: aiosqlite.Connection,
    query: str,
    limit: int,
    offset: int,
) -> tuple[list[DTCSearchResult], int]:
    cursor = await db.execute(
        "SELECT COUNT(*) as cnt FROM dtc_fts WHERE dtc_fts MATCH ?",
        (query,),
    )
    row = await cursor.fetchone()
    total = row["cnt"]

    cursor = await db.execute(
        "SELECT fc.code, fc.title, fc.subtitle "
        "FROM dtc_fts f "
        "JOIN dtc_fts_content fc ON fc.id = f.rowid "
        "WHERE dtc_fts MATCH ? "
        "LIMIT ? OFFSET ?",
        (query, limit, offset),
    )
    rows = await cursor.fetchall()
    items = [
        DTCSearchResult(
            code=r["code"],
            title=r["title"],
            subtitle=r["subtitle"],
        )
        for r in rows
    ]

    return items, total
