from typing import Type, TypeVar

import akeneo.models as models
from akeneo.client.client import Client
from dacite import from_dict

T = TypeVar("T")


class CacheBase:
    def __init__(self, client: Client) -> None:
        self._client = client

        self._cache = {}

    # --------------------------------------------------------------------------

    @property
    def currencies(self) -> list[models.Currency]:
        return self._get_from_cache_or_api("pim_api_currency_list", models.Currency)

    @property
    def locales(self) -> list[models.Locale]:
        return self._get_from_cache_or_api("pim_api_locale_list", models.Locale)

    # --------------------------------------------------------------------------

    def _get_from_cache_or_api(self, route_id: str, cls: Type[T]) -> list[T]:
        if not route_id in self._cache:
            self._cache[route_id] = self._get_from_api(route_id, cls)
        return self._cache[route_id]

    def _get_from_api(self, route_id: str, cls: Type[T]) -> list[T]:
        entries = self._client.get_list(route_id)
        return [from_dict(cls, entry) for entry in entries]
