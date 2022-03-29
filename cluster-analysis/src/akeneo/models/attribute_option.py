from dataclasses import dataclass

from .util import CodeAndLabel


@dataclass
class AttributeOption(CodeAndLabel):
    attribute: str
    sort_order: int
