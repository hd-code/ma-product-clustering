from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Locale:
    code: str
    enabled: bool
