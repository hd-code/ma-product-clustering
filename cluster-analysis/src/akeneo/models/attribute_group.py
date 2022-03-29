from dataclasses import dataclass

from .util import CodeAndLabel


@dataclass
class AttributeGroup(CodeAndLabel):
    attributes: list[str]
    sort_order: int
