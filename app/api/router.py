from __future__ import annotations

from fastapi import APIRouter

from app.api import components, dtc, stats

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(dtc.router)
api_router.include_router(components.router)
api_router.include_router(stats.router)
