from dataclasses import dataclass

from .locale import LocalStr


@dataclass
class Channel:
    code: str
    labels: LocalStr

    category_tree: str
    conversion_units: dict
    currencies: list[str]
    locales: list[str]