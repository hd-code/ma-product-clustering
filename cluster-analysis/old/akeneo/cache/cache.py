import akeneo.models as models
from akeneo.cache.cache_base import CacheBase
from akeneo.cache.cache_meta import CacheMeta
from akeneo.cache.cache_products import CacheProducts
from akeneo.client.client import Client


class Cache:
    def __init__(
        self, client: Client, locale: str, currency: str, channel: str
    ) -> None:
        self._client = client
        self._locale = locale
        self._currency = currency
        self._channel = channel

        self._cache_base = CacheBase(client)
        self._cache_meta = CacheMeta(client, locale)
        self._cache_products = CacheProducts(
            client, self._cache_meta, locale, currency, channel
        )

    # --------------------------------------------------------------------------

    def check(self) -> None:
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

    # --------------------------------------------------------------------------

    @property
    def attributes(self) -> list[models.Attribute]:
        return self._cache_meta.attributes

    @property
    def categories(self) -> list[models.Category]:
        return self._cache_meta.categories

    @property
    def client(self) -> Client:
        return self._client

    @property
    def families(self) -> list[models.Family]:
        return self._cache_meta.families

    @property
    def products(self) -> list[models.Product]:
        return self._cache_products.products
