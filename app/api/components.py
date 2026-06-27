from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from app.core.pagination import PaginatedResponse, PaginationParams, build_pagination_meta
from app.db.session import get_db
from app.schemas.component import Component, ComponentDetail
from app.services import component_service

router = APIRouter(prefix="/components", tags=["components"])


@router.get(
    "",
    response_model=PaginatedResponse[Component],
    summary="List all components",
    description="Returns a paginated list of all known VAG component identifiers.",
)
async def list_components(
    pagination: PaginationParams = Depends(),
    db=Depends(get_db),
) -> PaginatedResponse[Component]:
    items, total = await component_service.list_components(
        db, pagination.per_page, pagination.offset
    )
    meta = build_pagination_meta(pagination.page, pagination.per_page, total)
    return PaginatedResponse(items=items, pagination=meta)


@router.get(
    "/{identifier}",
    response_model=ComponentDetail,
    summary="Get component detail",
    description=(
        "Returns detail for a specific VAG component including all associated DTC codes. "
        "Component identifiers are case-insensitive (e.g., 'g47' and 'G47' both work)."
    ),
)
async def get_component(identifier: str, db=Depends(get_db)) -> ComponentDetail:
    result = await component_service.get_by_identifier(db, identifier)
    if not result:
        raise HTTPException(status_code=404, detail=f"Component '{identifier.upper()}' not found")
    return result
