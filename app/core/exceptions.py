from __future__ import annotations


class DTCNotFoundError(Exception):
    def __init__(self, code: str) -> None:
        self.code = code
        super().__init__(f"DTC code '{code}' not found")


class ComponentNotFoundError(Exception):
    def __init__(self, identifier: str) -> None:
        self.identifier = identifier
        super().__init__(f"Component '{identifier}' not found")
