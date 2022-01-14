from __future__ import annotations
from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional, Union


AkeneoProductValue = Union[date, bool, float, str, list[str], None]
AkeneoProductValues = dict[str, AkeneoProductValue]


@dataclass
class AkeneoProduct:
    identifier: str
    enabled: bool
    family: Optional[str]
    categories: list[str]
    groups: list[str]
    parent: Optional[str]
    values: AkeneoProductValues
    created: datetime
    updated: datetime
    associations: dict[str, dict]
    quantified_associations: dict

    @staticmethod
    def get_products_values(products: list[AkeneoProduct]) -> list[AkeneoProductValues]:
        return [product.values for product in products]
