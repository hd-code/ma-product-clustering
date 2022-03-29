from dataclasses import dataclass

from .util import CodeAndLabel


@dataclass
class Channel(CodeAndLabel):
    category_tree: str
    conversion_units: dict
    currencies: list[str]
    locales: list[str]
