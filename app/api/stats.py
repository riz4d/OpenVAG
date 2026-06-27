from __future__ import annotations

from fastapi import APIRouter, Depends

from app.db.session import get_db
from app.schemas.stats import StatsResponse

router = APIRouter(prefix="/stats", tags=["stats"])


@router.get(
    "",
    response_model=StatsResponse,
    summary="Database statistics",
    description="Returns row counts for all major tables in the database.",
)
async def get_stats(db=Depends(get_db)) -> StatsResponse:
    tables = ["dtc_codes", "dtc_variants", "components", "dtc_components", "related_codes"]
    counts: dict[str, int] = {}

    for table in tables:
        cursor = await db.execute(f"SELECT COUNT(*) as cnt FROM {table}")
        row = await cursor.fetchone()
        counts[table] = row["cnt"]

    return StatsResponse(
        dtc_codes=counts["dtc_codes"],
        dtc_variants=counts["dtc_variants"],
        components=counts["components"],
        dtc_components=counts["dtc_components"],
        related_codes=counts["related_codes"],
    )
