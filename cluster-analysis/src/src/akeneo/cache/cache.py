import json
from pathlib import Path
from typing import Any, TypeVar

from .. import models
from .files import FileInfo, Files
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

        attr_data = self._load_file(data_dir / Files.ATTRIBUTES.value.filename)
        meas_data = self._load_file(data_dir / Files.MEASUREMENTS.value.filename)

        self._parser = Parser(locale, currency, channel, attr_data, meas_data)

    # --------------------------------------------------------------------------

    @property
    def attribute_groups(self) -> list[models.AttributeGroup]:
        return self._load_and_parse(Files.ATTRIBUTE_GROUPS.value)

    @property
    def attributes(self) -> list[models.Attribute]:
        return self._load_and_parse(Files.ATTRIBUTES.value)

    @property
    def categories(self) -> list[models.Category]:
        return self._load_and_parse(Files.CATEGORIES.value)

    @property
    def channels(self) -> list[models.Channel]:
        return self._load_and_parse(Files.CHANNELS.value)

    @property
    def currencies(self) -> list[models.Currency]:
        return self._load_and_parse(Files.CURRENCIES.value)

    @property
    def families(self) -> list[models.Family]:
        return self._load_and_parse(Files.FAMILIES.value)

    @property
    def locales(self) -> list[models.Locale]:
        return self._load_and_parse(Files.LOCALES.value)

    @property
    def measurements(self) -> list[models.MeasurementFamily]:
        return self._load_and_parse(Files.MEASUREMENTS.value)

    @property
    def products(self) -> list[models.Product]:
        return self._load_and_parse(Files.PRODUCTS.value)

    # --------------------------------------------------------------------------

    def _load_file(self, filepath: Path) -> Any:
        file = open(filepath, "r")
        return json.load(file)

    def _load_and_parse(self, fileinfo: FileInfo) -> list[T]:
        filepath = self._data_dir / fileinfo.filename
        data = self._load_file(filepath)
        return self._parser.parse_list(data, fileinfo.model_cls)
