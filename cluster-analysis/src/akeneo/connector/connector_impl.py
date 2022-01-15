from __future__ import annotations
from datetime import datetime
from typing import TypeVar

from dacite import from_dict
from dacite.config import Config

from .client import Client
from .connector import Connector
import akeneo.models as models


T = TypeVar("T")


class ConnectorImpl(Connector):
    def __init__(
        self,
        client: Client,
        preferred_channel: str = "ecommerce",
        locale: str = "en_US",
        check: bool = True
    ) -> None:
        self._client = client
        self._preferred_channel = preferred_channel
        self._locale = locale
        if check:
            self._check()

    # public -------------------------------------------------------------------

    def get_attributes(self) -> list[models.Attribute]:
        return self.attributes

    def get_categories(self) -> list[models.Category]:
        return self.categories

    def get_families(self) -> list[models.Family]:
        return self.families

    def get_products(self) -> list[models.Product]:
        return self.products

    # data & cache -------------------------------------------------------------

    @property
    def attributes(self) -> list[models.Attribute]:
        if not hasattr(self, "_attributes"):
            route_id = "pim_api_attribute_list"
            config = Config(
                type_hooks={models.LocalStr: self._translate},
                cast=[models.AttributeType],
            )
            self._attributes = self._get_list_from_api(
                route_id, models.Attribute, config)
        return self._attributes

    @property
    def attributes_dict(self) -> dict[str, models.Attribute]:
        if not hasattr(self, "_attributes_dict"):
            self._attributes_dict: dict[str, models.Attribute] = {}
            for attr in self.attributes:
                self._attributes_dict[attr.code] = attr
        return self._attributes_dict

    @property
    def categories(self) -> list[models.Category]:
        if not hasattr(self, "_categories"):
            route_id = "pim_api_category_list"
            config = Config(type_hooks={models.LocalStr: self._translate})
            self._categories = self._get_list_from_api(
                route_id, models.Category, config)
        return self._categories

    @property
    def channels(self) -> list[dict]:
        if not hasattr(self, "_channels"):
            self._channels = self._client.get_list("pim_api_channel_list")
        return self._channels

    @property
    def families(self) -> list[models.Family]:
        if not hasattr(self, "_families"):
            route_id = "pim_api_family_list"
            config = Config(type_hooks={models.LocalStr: self._translate})
            self._families = self._get_list_from_api(
                route_id, models.Family, config)
        return self._families

    @property
    def locales(self) -> list[dict]:
        if not hasattr(self, "_locales"):
            self._locales = self._client.get_list("pim_api_locale_list")
        return self._locales

    @property
    def products(self) -> list[models.Product]:
        if not hasattr(self, "_products"):
            route_id = "pim_api_product_list"
            params = {"locales": self._locale}
            config = Config(type_hooks={
                datetime: datetime.fromisoformat,
                models.ProductValues: self._extract_values,
            })
            self._products = self._get_list_from_api(
                route_id, models.Product, config, params)
        return self._products

    # check --------------------------------------------------------------------

    def _check(self) -> None:
        self._check_locale()
        self._check_channel()

    def _check_channel(self) -> None:
        for channel in self.channels:
            if channel["code"] == self._preferred_channel:
                if not self._locale in channel["locales"]:
                    raise ValueError(
                        "selected locale is not available in preferred channel")
                return None
        raise ValueError("channel does not exist")

    def _check_locale(self) -> None:
        for locale in self.locales:
            if locale["code"] == self._locale:
                if not locale["enabled"]:
                    raise ValueError("locale is not enabled in akeneo pim")
                return None
        raise ValueError("locale unknown")

    # data access and mapping --------------------------------------------------

    def _get_list_from_api(self, route_id: str, cls: T, config: Config, params: dict = None) -> list[T]:
        res = self._client.get_list(route_id, params=params)
        result = []
        for res_entry in res:
            entry = from_dict(cls, res_entry, config)
            result.append(entry)
        return result

    def _translate(self, locales: dict | None) -> str:
        try:
            return locales[self._locale]
        except:
            return ""

    def _extract_values(self, values: dict[list]) -> models.ProductValues:
        result: models.ProductValues = {}
        for key, value in values.items():
            result[key] = self._extract_value(key, value)
        return result

    def _extract_value(self, attr_code: str, value: list[dict]):
        if len(value) == 0:
            return None

        attr = self.attributes_dict[attr_code]
        if len(value) == 1:
            data = value[0]["data"]
            return self._map_attr_type_to_handler[attr.type](data)

        index = 0
        for i in range(len(value)):
            entry = value[i]
            if entry["scope"] == self._preferred_channel:
                index = i
                break
        data = value[index]["data"]
        return self._map_attr_type_to_handler[attr.type](data)

    _map_attr_type_to_handler: dict[models.AttributeType] = {
        models.AttributeType.ID: lambda x: x,
        models.AttributeType.TEXT: lambda x: x,
        models.AttributeType.TEXTAREA: lambda x: x,
        models.AttributeType.SELECT_SINGLE: lambda x: x,
        models.AttributeType.SELECT_MULTI: lambda x: x,
        models.AttributeType.BOOL: lambda x: x,
        models.AttributeType.DATE: datetime.fromisoformat,
        models.AttributeType.NUMBER: lambda x: x,
        # TODO !!!
        models.AttributeType.METRIC: lambda x: x["amount"],
        models.AttributeType.PRICE: lambda x: x[0]["amount"],
        models.AttributeType.IMAGE: lambda x: x,
        models.AttributeType.FILE: lambda x: x,
        models.AttributeType.REFERENCE_SINGLE: lambda x: x,
        models.AttributeType.REFERENCE_MULTI: lambda x: x,
    }
