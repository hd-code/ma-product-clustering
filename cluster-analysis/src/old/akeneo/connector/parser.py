from datetime import datetime
from typing import Any, Callable, Optional, Type, TypeVar

from dacite import Config, from_dict

from .. import client, models

T = TypeVar("T")


class Parser:
    def __init__(
        self, client: client.Client, locale: str, currency: str, channel: str
    ) -> None:
        self._client = client
        self._locale = locale
        self._currency = currency
        self._channel = channel

        self._cache = {}

    # --------------------------------------------------------------------------

    def get_attributes(self) -> list[models.Attribute]:
        return self._get_list_from_api("pim_api_attribute_list", models.Attribute)

    def get_categories(self) -> list[models.Category]:
        return self._get_list_from_api("pim_api_category_list", models.Category)

    def get_channels(self) -> list[models.Channel]:
        return self._get_list_from_api("pim_api_channel_list", models.Channel)

    def get_families(self) -> list[models.Family]:
        return self._get_list_from_api("pim_api_family_list", models.Family)

    def get_currencies(self) -> list[models.Currency]:
        return self._get_list_from_api("pim_api_currency_list", models.Currency)

    def get_locales(self) -> list[models.Locale]:
        return self._get_list_from_api("pim_api_locale_list", models.Locale)

    def get_measurement_families(self) -> list[models.MeasurementFamily]:
        route_id = "pim_api_measurement_family_get"
        entries = self._client.get(route_id)
        return [
            from_dict(models.MeasurementFamily, entry, self._config)
            for entry in entries
        ]

    # --------------------------------------------------------------------------

    def _get_list_from_api(self, route_id: str, cls: Type[T]) -> list[T]:
        entries = self._client.get_list(route_id)
        return [from_dict(cls, entry, self._config) for entry in entries]

    @property
    def _config(self) -> Config:
        self._cache = {}
        return Config(
            cast=[bool, float, int, models.AttributeType],
            type_hooks={
                datetime: datetime.fromisoformat,
                models.LocalStr: self._translate,
                models.ProductValues: self._handle_values,
            },
        )

    @property
    def _attributes(self) -> dict[str, models.Attribute]:
        return self._get_or_add_dict_to_cache("attributes", self.get_attributes, "code")

    @property
    def _measurements(self) -> dict[str, models.MeasurementFamily]:
        return self._get_or_add_dict_to_cache(
            "measurements", self.get_measurement_families, "code"
        )

    def _get_or_add_dict_to_cache(
        self, cache_key: str, get_func: Callable[[], list[T]], key_prop: str
    ) -> dict[str, T]:
        if cache_key not in self._cache:
            entries = get_func()
            self._cache[cache_key] = {}
            for entry in entries:
                self._cache[cache_key][entry[key_prop]] = entry
        return self._cache[cache_key]

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
