from __future__ import annotations
from typing import TypeVar

from .cache_base import CacheBase
from .cache_meta import CacheMeta
from .cache_products import CacheProducts
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
        currency: str = "USD",
        check: bool = True
    ) -> None:
        self._client = client
        self._channel = preferred_channel
        self._currency = currency
        self._locale = locale

        self._cache_base = CacheBase(client)
        self._cache_meta = CacheMeta(client, locale)
        self._cache_products = CacheProducts(
            client, self._cache_meta, locale, currency, preferred_channel)

        if check:
            self._check()

    # --------------------------------------------------------------------------

    def get_attributes(self) -> list[models.Attribute]:
        return self._cache_meta.attributes

    def get_categories(self) -> list[models.Category]:
        return self._cache_meta.categories

    def get_families(self) -> list[models.Family]:
        return self._cache_meta.families

    def get_products(self) -> list[models.Product]:
        return self._cache_products.products

    # --------------------------------------------------------------------------

    def _check(self) -> None:
        self._check_locale()
        self._check_currency()
        self._check_channel()

    def _check_channel(self) -> None:
        for channel in self._cache_meta.channels:
            if channel.code == self._channel:
                if not self._locale in channel.locales:
                    raise ValueError("locale not available in channel")
                if not self._currency in channel.currencies:
                    raise ValueError("currency not available in channel")
                return None
        raise ValueError("channel unknown")

    def _check_currency(self) -> None:
        for currency in self._cache_base.currencies:
            if currency.code == self._currency:
                if not currency.enabled:
                    raise ValueError("currency is not enabled in akeneo pim")
                return None
        raise ValueError("currency unknown")

    def _check_locale(self) -> None:
        for locale in self._cache_base.locales:
            if locale.code == self._locale:
                if not locale.enabled:
                    raise ValueError("locale is not enabled in akeneo pim")
                return None
        raise ValueError("locale unknown")
