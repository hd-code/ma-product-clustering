from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Type, TypeVar

from .. import models
from .parser import Parser

T = TypeVar("T")


class Cache:
    def __init__(
        self,
        data_dir: Path,
        locale: str = "en_US",
        currency: str = "USD",
        channel: str = "default",
    ) -> None:
        self._data_dir = data_dir

        attr_data = self._load_file(data_dir / "attributes.json")
        meas_data = self._load_file(data_dir / "measurements.json")

        self._parser = Parser(locale, currency, channel, attr_data, meas_data)

    def get_attributes(self) -> list[models.Attribute]:
        return self._load_and_parse("attributes.json", models.Attribute)

    def get_categories(self) -> list[models.Category]:
        return self._load_and_parse("categories.json", models.Category)

    def get_channels(self) -> list[models.Channel]:
        return self._load_and_parse("channels.json", models.Channel)

    def get_currencies(self) -> list[models.Currency]:
        return self._load_and_parse("currencies.json", models.Currency)

    def get_families(self) -> list[models.Family]:
        return self._load_and_parse("families.json", models.Family)

    def get_measurements(self) -> list[models.MeasurementFamily]:
        return self._load_and_parse(
            "measurement-families.json", models.MeasurementFamily
        )

    def get_products(self) -> list[models.Product]:
        return self._load_and_parse("products.json", models.Product)

    # --------------------------------------------------------------------------

    def _load_file(self, filepath: Path) -> Any:
        file = open(filepath, "r")
        return json.load(file)

    def _load_and_parse(self, filename: str, cls: Type[T]) -> list[T]:
        filepath = self._data_dir / filename
        data = self._load_file(filepath)
        return self._parser.parse_list(data, cls)
