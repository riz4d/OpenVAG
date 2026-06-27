from __future__ import annotations

from pydantic import BaseModel


class DTCVariant(BaseModel):
    subtitle: str | None = None
    symptoms: list[str]
    causes: list[str]
    solutions: list[str]
    special_notes: str | None = None


class DTCCode(BaseModel):
    code: str
    title: str


class DTCDetail(BaseModel):
    code: str
    title: str
    variants: list[DTCVariant]
    components: list[str]
    related_codes: list[str]


class DTCSearchResult(BaseModel):
    code: str
    title: str
    subtitle: str | None = None
