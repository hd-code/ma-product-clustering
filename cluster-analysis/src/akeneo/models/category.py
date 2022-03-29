from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from .util import CodeAndLabel


@dataclass
class Category(CodeAndLabel):
    parent: Optional[str]
