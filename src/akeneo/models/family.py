from __future__ import annotations
from dataclasses import dataclass

from akeneo.models.util import LocalStr


@dataclass
class AkeneoFamily:
    code: str
    attributes: list[str]
    labels: LocalStr
