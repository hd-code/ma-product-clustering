from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Optional


@dataclass
class ProductValue:
    locale: Optional[str]
    scope: Optional[str]
    data: Any


@dataclass
class Product:
    identifier: str
    enabled: bool

    family: Optional[str]
    categories: list[str]
    groups: list[str]

    created: datetime
    updated: datetime

    parent: Optional[str]

    # associations: dict[str, dict]
    # quantified_associations: dict

    values: dict[str, list[ProductValue]]
