from __future__ import annotations

import time

from fastapi import APIRouter, Depends

from app.core.config import settings
from app.db.session import get_db
from app.schemas.health import HealthResponse

router = APIRouter(tags=["health"])

_start_time: float = time.time()


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health check",
    description="Returns application health status including DB connectivity and uptime.",
)
async def health_check(db=Depends(get_db)) -> HealthResponse:
    uptime = int(time.time() - _start_time)
    try:
        cursor = await db.execute("SELECT COUNT(*) as cnt FROM dtc_codes")
        row = await cursor.fetchone()
        dtc_count = row["cnt"]
        database_status = "connected"
        status = "healthy"
    except Exception:
        dtc_count = 0
        database_status = "disconnected"
        status = "unhealthy"

    response = HealthResponse(
        status=status,
        version=settings.API_VERSION,
        database=database_status,
        uptime=uptime,
        dtc_count=dtc_count,
    )

    if status == "unhealthy":
        from fastapi.responses import JSONResponse

        return JSONResponse(content=response.model_dump(), status_code=503)

    return response
