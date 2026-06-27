from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query

from app.core.pagination import PaginatedResponse, PaginationParams, build_pagination_meta
from app.db.session import get_db
from app.schemas.dtc import DTCCode, DTCDetail, DTCSearchResult
from app.services import dtc_service

router = APIRouter(prefix="/dtc", tags=["dtc"])


@router.get(
    "",
    response_model=PaginatedResponse[DTCCode],
    summary="List all DTC codes",
    description="Returns a paginated list of all DTC codes in the database.",
)
async def list_dtc(
    pagination: PaginationParams = Depends(),
    db=Depends(get_db),
) -> PaginatedResponse[DTCCode]:
    items, total = await dtc_service.list_codes(db, pagination.per_page, pagination.offset)
    meta = build_pagination_meta(pagination.page, pagination.per_page, total)
    return PaginatedResponse(items=items, pagination=meta)


@router.get(
    "/search",
    response_model=PaginatedResponse[DTCSearchResult],
    summary="Search DTC codes",
    description=(
        "Full-text search across all DTC fields (code, title, symptoms, causes, solutions). "
        "Uses porter-stemmed tokenization for flexible matching."
    ),
)
async def search_dtc(
    q: str = Query(..., min_length=1, description="Search query"),
    pagination: PaginationParams = Depends(),
    db=Depends(get_db),
) -> PaginatedResponse[DTCSearchResult]:
    items, total = await dtc_service.search(db, q, pagination.per_page, pagination.offset)
    meta = build_pagination_meta(pagination.page, pagination.per_page, total)
    return PaginatedResponse(items=items, pagination=meta)


@router.get(
    "/{code}",
    response_model=DTCDetail,
    summary="Get DTC detail",
    description=(
        "Returns full detail for a specific DTC code including all variants, "
        "associated components, and cross-referenced related codes."
    ),
)
async def get_dtc(code: str, db=Depends(get_db)) -> DTCDetail:
    result = await dtc_service.get_by_code(db, code)
    if not result:
        raise HTTPException(status_code=404, detail=f"DTC code '{code}' not found")
    return result
