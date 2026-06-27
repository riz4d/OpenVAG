from __future__ import annotations

from pydantic import BaseModel


class StatsResponse(BaseModel):
    dtc_codes: int
    dtc_variants: int
    components: int
    dtc_components: int
    related_codes: int
