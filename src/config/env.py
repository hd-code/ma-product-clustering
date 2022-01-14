import os

from dotenv import dotenv_values

from config.paths import base_path


class _Env:
    def __init__(self) -> None:
        self.env = {
            **dotenv_values(base_path / ".env"),
            **os.environ,  # override loaded values with environment variables
        }

    def __call__(self) -> dict[str, str]:
        return self.env


get_env = _Env()
