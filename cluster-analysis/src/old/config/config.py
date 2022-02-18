import os
from pathlib import Path

from dotenv import dotenv_values

dir_base = Path(__file__).parent.parent.parent.resolve()
dir_data = dir_base / "data"

env = {
    **dotenv_values(dir_base / ".env"),
    **os.environ,  # overwrite from environment
}
