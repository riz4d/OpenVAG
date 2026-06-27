from __future__ import annotations

from dataclasses import dataclass


@dataclass
class DTCCodeRow:
    id: int
    code: str
    title: str


@dataclass
class DTCVariantRow:
    id: int
    dtc_code_id: int
    subtitle: str | None
    symptoms: str | None
    causes: str | None
    solutions: str | None
    special_notes: str | None


@dataclass
class ComponentRow:
    id: int
    identifier: str
    description: str | None


@dataclass
class RelatedCodeRow:
    id: int
    dtc_code_id: int
    related_code: str


@dataclass
class FTSResultRow:
    code: str
    title: str
    subtitle: str | None
    dtc_code_id: int
    variant_id: int
