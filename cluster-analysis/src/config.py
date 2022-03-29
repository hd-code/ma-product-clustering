import os
from pathlib import Path

from dotenv import dotenv_values

dir_base = Path(__file__).parent.parent.resolve()
dir_data = dir_base / "data"

env: dict[str, str] = {
    **dotenv_values(dir_base / ".env"),  # type:ignore
    **os.environ,  # overwrite from environment
}
