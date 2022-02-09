from datetime import datetime
from typing import Any, Callable, Optional, Type, TypeVar

from dacite import from_dict
from dacite.config import Config

from .. import models

T = TypeVar("T")


class Parser:
    def __init__(
        self, locale: str, currency: str, channel: str, attr_data, measurements_data
    ) -> None:
        self._locale = locale
        self._currency = currency
        self._channel = channel

        self._attributes = self._parse_list_to_dict(attr_data, models.Attribute, "code")
        self._measurements = self._parse_list_to_dict(
            measurements_data, models.MeasurementFamily, "code"
        )

    def parse_list(self, data: Any, data_cls: Type[T]) -> list[T]:
        return [from_dict(data_cls, d, self._config) for d in data]

    # --------------------------------------------------------------------------

    def _parse_list_to_dict(
        self, data: Any, data_cls: Type[T], key_prop: str
    ) -> dict[str, T]:
        config = Config(cast=[bool, float, int, models.AttributeType])
        entries = [from_dict(data_cls, d, config) for d in data]
        result = {}
        for entry in entries:
            key = entry[key_prop]
            result[key] = entry
        return result

    @property
    def _config(self) -> Config:
        return Config(
            cast=[bool, float, int, models.AttributeType],
            type_hooks={
                datetime: datetime.fromisoformat,
                models.LocalStr: self._translate,
                models.ProductValues: self._handle_values,
            },
        )

    # --------------------------------------------------------------------------

    def _translate(self, locales: Optional[dict]) -> str:
        try:
            return locales[self._locale]
        except:
            return ""

    def _handle_values(self, values: dict[str, list[dict]]) -> models.ProductValues:
        result: models.ProductValues = {}
        for attr_code, value in values.items():
            attribute = self._attributes[attr_code]
            result[attr_code] = self._handle_value(attribute, value)
        return result

    def _handle_value(
        self, attribute: models.Attribute, value: list[dict]
    ) -> models.ProductValue:
        if not value:
            return None

        index = 0
        if len(value) > 1:
            for i in range(1, len(value)):
                if value[i]["scope"] in [None, self._channel]:
                    index = i

        return self._handle_data(attribute, value[index]["data"])

    def _handle_data(self, attribute: models.Attribute, data) -> models.ProductValue:
        if data == None:
            return None
        if attribute.type == models.AttributeType.METRIC:
            return self._handle_metric(attribute, data)
        if attribute.type == models.AttributeType.PRICE:
            return self._handle_price(data)
        return self._map_attr_type_to_handler[attribute.type](data)

    def _handle_metric(self, attribute: models.Attribute, data: dict) -> float:
        amount = float(data["amount"])
        unit = data["unit"]
        measurement_family = self._measurements[attribute.metric_family]
        return measurement_family.convert(amount, unit, attribute.default_metric_unit)

    def _handle_price(self, data: list[dict]) -> float:
        if not data:
            return None

        index = 0
        if len(data) > 1:
            for i in range(1, len(data)):
                if data[i]["currency"] == self._currency:
                    index = i

        return float(data[index]["amount"])

    _map_attr_type_to_handler: dict[
        models.AttributeType, Callable[[Any], models.ProductValue]
    ] = {
        models.AttributeType.ID: str,
        models.AttributeType.TEXT: str,
        models.AttributeType.TEXTAREA: str,
        models.AttributeType.SELECT_SINGLE: str,
        models.AttributeType.SELECT_MULTI: lambda x: [str(y) for y in x],
        models.AttributeType.BOOL: bool,
        models.AttributeType.DATE: datetime.fromisoformat,
        models.AttributeType.NUMBER: float,
        models.AttributeType.IMAGE: str,
        models.AttributeType.FILE: str,
        models.AttributeType.REFERENCE_SINGLE: str,
        models.AttributeType.REFERENCE_MULTI: lambda x: [str(y) for y in x],
    }
