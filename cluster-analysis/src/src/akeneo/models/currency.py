from dataclasses import dataclass


@dataclass
class Currency:
    code: str
    enabled: bool
