from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import NewType, Optional, Union

from .attribute import Attribute, AttributeType


# prevents dacite from trying to cast ProductValue as datetime
_DatetimeAlias = NewType("_DatetimeAlias", datetime)

ProductValue = Union[_DatetimeAlias, bool, float, str, list[str], None]
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
    def to_products_values(attributes: list[Attribute], products: list[Product]) -> list[ProductValues]:
        id_name = "__identifier__"
        for attribute in attributes:
            if attribute.type == AttributeType.ID:
                id_name = attribute.code
                break
        return [{id_name: product.identifier, **product.values} for product in products]
