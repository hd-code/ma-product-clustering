from dataclasses import dataclass

from .locale import LocalStr


@dataclass
class AttributeGroup:
    code: str
    labels: LocalStr
    sort_order: int
    attributes: list[str]
