from dataclasses import dataclass


@dataclass
class CodeAndLabel:
    code: str
    labels: dict[str, str]

    def get_label(self, locale: str) -> str:
        return self.labels.get(locale, f"[{self.code}]")
