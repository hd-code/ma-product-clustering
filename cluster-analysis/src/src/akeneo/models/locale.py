from dataclasses import dataclass
from typing import NewType

LocalStr = NewType("LocalStr", str)


@dataclass
class Locale:
    code: str
    enabled: bool
