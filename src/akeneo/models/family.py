from __future__ import annotations
from dataclasses import dataclass

from .util import LocalStr


@dataclass
class Family:
    code: str
    labels: LocalStr
    attributes: list[str]
    # attribute_as_label: str
    # attribute_as_image: str
    # attribute_requirements: dict[str, list[str]]
