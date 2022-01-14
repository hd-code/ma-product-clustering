from __future__ import annotations
from pathlib import Path

import toml


def load_dependencies_from_pipfile(filepath: Path, ignore_packages: set[str] = {}) -> list[str]:
    pipfile = toml.load(filepath)
    packages: dict[str, str | dict] = pipfile["packages"]
    result: list[str] = []
    for pkg, version in packages.items():
        if not isinstance(version, str) or pkg in ignore_packages:
            continue
        res = f"{pkg}{version}" if version != "*" else pkg
        result.append(res)
    return result


# for testing
if __name__ == "__main__":
    pipfile_path = Path(__file__).parent.parent / "Pipfile"
    ignore = {"jupyter", "matplotlib", "numpy", "pandas", "toml"}

    result = load_dependencies_from_pipfile(pipfile_path, ignore)
    print(result)
