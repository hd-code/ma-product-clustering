from typing import Type, TypeVar

from dacite import from_dict

from .client import Client
import akeneo.models as models


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
        if not hasattr(self._cache, route_id):
            self._cache[route_id] = self._get_from_api(route_id, cls)
        return self._cache[route_id]

    def _get_from_api(self, route_id: str, cls: Type[T]) -> list[T]:
        entries = self._client.get_list(route_id)
        return [from_dict(cls, entry) for entry in entries]
