import json
from datetime import datetime
from pathlib import Path
from typing import Any, Type, TypeVar

from dacite import Config, from_dict

from .. import models
from .files import ATTRIBUTE_OPTIONS_DIR_NAME, FileInfo

T = TypeVar("T")


class Loader:
    def __init__(self, data_dir: Path) -> None:
        self._data_dir = data_dir

    # --------------------------------------------------------------------------

    def load(self, fileinfo: FileInfo) -> list[T]:
        filepath = self._data_dir / fileinfo.filename
        data = self._load_file(filepath)
        return self._parse_list(data, fileinfo.model_cls)

    def load_attribute_options(self, attr_code: str) -> list[models.AttributeOption]:
        filepath = self._data_dir / ATTRIBUTE_OPTIONS_DIR_NAME / f"{attr_code}.json"
        data = self._load_file(filepath)
        return self._parse_list(data, models.AttributeOption)

    # --------------------------------------------------------------------------

    def _load_file(self, filepath: Path) -> list[Any]:
        with open(filepath, "r") as file:
            data = json.load(file)
        return data

    def _parse_list(self, data: list[Any], data_cls: Type[T]) -> list[T]:
        return [from_dict(data_cls, d, self._config) for d in data]

    @property
    def _config(self) -> Config:
        return Config(
            cast=[bool, float, int, models.AttributeType],
            type_hooks={
                datetime: datetime.fromisoformat,
            },
        )
