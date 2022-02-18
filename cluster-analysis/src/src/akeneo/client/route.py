from dataclasses import dataclass, field
from typing import Literal

RestMethods = Literal["GET", "POST", "PATCH", "DELETE"]
PathVars = dict[str, str]


@dataclass
class Route:
    id: str
    path: str
    method: RestMethods
    path_vars: list[str] = field(init=False)

    def __post_init__(self):
        path_vars: list[str] = []
        for path_part in self.path.split("/"):
            if path_part and path_part[0] == "{":
                path_vars.append(path_part.strip("{}"))
        self.path_vars = path_vars

    def make_path(self, path_vars: PathVars):
        path_parts = self.path.split("/")
        for i in range(len(path_parts)):
            path_part = path_parts[i]
            if path_part and path_part[0] == "{":
                assert path_vars, "`path_vars` are missing"
                path_code = path_part.strip("{}")
                assert (
                    path_code in path_vars
                ), f"key '{path_code}' is missing in `path_vars`"
                path_parts[i] = path_vars[path_code]
        return "/".join(path_parts)
