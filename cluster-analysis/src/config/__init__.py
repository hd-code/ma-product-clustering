import os
from pathlib import Path

from dotenv import dotenv_values


_base_path = Path(__file__).parent.parent.parent.resolve()

data_dir = _base_path / "data"

env = {
    **dotenv_values(_base_path / ".env"),
    **os.environ,  # override loaded values with environment variables
}
