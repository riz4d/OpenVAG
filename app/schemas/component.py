from __future__ import annotations

from pydantic import BaseModel


class Component(BaseModel):
    identifier: str
    description: str | None = None


class ComponentDTCCode(BaseModel):
    code: str
    title: str


class ComponentDetail(BaseModel):
    identifier: str
    description: str | None = None
    dtc_codes: list[ComponentDTCCode]
