from __future__ import annotations

from dataclasses import dataclass

from .util import CodeAndLabel


@dataclass
class Family(CodeAndLabel):
    attributes: list[str]
    attribute_requirements: dict[str, list[str]]
    # attribute_as_label: str
    # attribute_as_image: str
