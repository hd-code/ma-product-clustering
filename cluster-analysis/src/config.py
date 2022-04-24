import os
import pickle
from pathlib import Path
from typing import Callable, TypeVar

from dotenv import dotenv_values

dir_base = Path(__file__).parent.parent.resolve()
dir_data = dir_base / "data"

env: dict[str, str] = {
    **dotenv_values(dir_base / ".env"),  # type:ignore
    **os.environ,  # overwrite from environment
}

T = TypeVar("T")


def load_or_create(file: Path, create_func: Callable[[], T]) -> T:
    """Store the result of complex calculations in a file

    If the file with the data already exists, the results are loaded from the
    file. Otherwise, the complex calculation in `create_func` is executed and
    the results will be stored to `file`.
    """
    try:
        with open(file, "rb") as f:
            return pickle.load(f)
    except:
        data = create_func()
        with open(file, "wb") as f:
            pickle.dump(data, f)
        return data
