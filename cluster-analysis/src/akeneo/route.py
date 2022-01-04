from dataclasses import dataclass
from typing import Literal


RestMethods = Literal["GET", "POST", "PATCH", "DELETE"]


@dataclass(frozen=True)
class AkeneoRoute:
    id: str
    path: str
    method: RestMethods

    @property
    def path_vars(self) -> list[str]:
        result: list[str] = []
        for path_part in self.path.split("/"):
            if path_part and path_part[0] == "{":
                result.append(path_part.strip("{}"))
        return result

    @property
    def is_list(self) -> bool:
        return self.method == "GET" and self.id[-5:] == "_list"

    def make_path(self, path_vars: dict[str, str]):
        path_parts = self.path.split("/")
        for i in range(len(path_parts)):
            path_part = path_parts[i]
            if path_part and path_part[0] == "{":
                path_code = path_part.strip("{}")
                path_parts[i] = path_vars[path_code]
        return "/".join(path_parts)
