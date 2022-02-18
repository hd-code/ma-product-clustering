from dataclasses import dataclass


@dataclass
class Locale:
    code: str
    enabled: bool
