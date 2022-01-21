from datetime import datetime
from typing import Callable, Type, TypeVar, Any

from dacite import from_dict
from dacite.config import Config

from .cache_meta import CacheMeta
from .client import Client
import akeneo.models as models


T = TypeVar("T")


class CacheProducts:

    def __init__(self, client: Client, cache_meta: CacheMeta, locale: str, currency: str, channel: str) -> None:
        self._client = client

        self._locale = locale
        self._currency = currency
        self._channel = channel

        self._attributes: dict[str, models.Attribute] = {}
        for attribute in cache_meta.attributes:
            self._attributes[attribute.code] = attribute

        self._measurements: dict[str, models.MeasurementFamily] = {}
        for measurement in cache_meta.measurement_families:
            self._measurements[measurement.code] = measurement

        self._cache = {}

    # --------------------------------------------------------------------------

    @property
    def products(self) -> list[models.Product]:
        route_id = "pim_api_product_list"
        if not route_id in self._cache:
            params = {"locales": self._locale}
            products = self._get_from_api(route_id, models.Product, params)
            self._cache[route_id] = products
        return self._cache[route_id]

    # --------------------------------------------------------------------------

    def _get_from_api(self, route_id: str, cls: Type[T], params: dict = None) -> list[T]:
        entries = self._client.get_list(route_id, params=params)
        return [from_dict(cls, entry, self._config) for entry in entries]

    @property
    def _config(self) -> Config:
        return Config(
            type_hooks={
                datetime: datetime.fromisoformat,
                models.ProductValues: self._handle_values,
            },
        )

    def _handle_values(self, values: dict[str, list[dict]]) -> models.ProductValues:
        result: models.ProductValues = {}
        for attr_code, value in values.items():
            attribute = self._attributes[attr_code]
            result[attr_code] = self._handle_value(attribute, value)
        return result

    def _handle_value(self, attribute: models.Attribute, value: list[dict]) -> models.ProductValue:
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

    _map_attr_type_to_handler: dict[models.AttributeType, Callable[[Any], models.ProductValue]] = {
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
