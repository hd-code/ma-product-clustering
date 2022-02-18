from datetime import datetime
from typing import Optional, Type, TypeVar

import akeneo.models as models
from akeneo.client.client import Client
from dacite import from_dict
from dacite.config import Config

T = TypeVar("T")


class CacheMeta:
    def __init__(self, client: Client, locale: str) -> None:
        self._client = client
        self._locale = locale

        self._cache = {}

    # --------------------------------------------------------------------------

    @property
    def attributes(self) -> list[models.Attribute]:
        return self._get_from_cache_or_api("pim_api_attribute_list", models.Attribute)

    @property
    def categories(self) -> list[models.Category]:
        return self._get_from_cache_or_api("pim_api_category_list", models.Category)

    @property
    def channels(self) -> list[models.Channel]:
        return self._get_from_cache_or_api("pim_api_channel_list", models.Channel)

    @property
    def families(self) -> list[models.Family]:
        return self._get_from_cache_or_api("pim_api_family_list", models.Family)

    @property
    def measurement_families(self) -> list[models.MeasurementFamily]:
        route_id = "pim_api_measurement_family_get"
        if not route_id in self._cache:
            entries = self._client.get(route_id)
            self._cache[route_id] = [
                from_dict(models.MeasurementFamily, entry, self._config)
                for entry in entries
            ]
        return self._cache[route_id]

    # --------------------------------------------------------------------------

    def _get_from_cache_or_api(self, route_id: str, cls: Type[T]) -> list[T]:
        if not route_id in self._cache:
            self._cache[route_id] = self._get_from_api(route_id, cls)
        return self._cache[route_id]

    def _get_from_api(self, route_id: str, cls: Type[T]) -> list[T]:
        entries = self._client.get_list(route_id)
        return [from_dict(cls, entry, self._config) for entry in entries]

    @property
    def _config(self) -> Config:
        return Config(
            cast=[bool, float, int, models.AttributeType],
            type_hooks={
                datetime: datetime.fromisoformat,
                models.LocalStr: self._translate,
            },
        )

    def _translate(self, locales: Optional[dict]) -> str:
        try:
            return locales[self._locale]
        except:
            return ""
