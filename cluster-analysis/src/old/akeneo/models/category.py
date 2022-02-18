from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from .util import LocalStr


@dataclass
class Category:
    code: str
    labels: LocalStr
    parent: Optional[str]
