from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

from akeneo.models.util import LocalStr


@dataclass
class AkeneoCategory:
    code: str
    parent: Optional[str]
    labels: LocalStr
