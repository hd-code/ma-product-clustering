from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Optional, Union


ProductValue = Union[date, bool, float, str, list[str], None]
ProductValues = dict[str, ProductValue]


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
    values: ProductValues = field(repr=False)

    @staticmethod
    def to_products_values(products: list[Product]) -> list[ProductValues]:
        return [product.values for product in products]
