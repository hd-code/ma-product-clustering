from __future__ import annotations

import pickle as pk
from pathlib import Path
from typing import TypeVar

import akeneo.models as models
from akeneo.cache.cache import Cache
from akeneo.client.client import Client
from akeneo.connector.connector import Connector

T = TypeVar("T")


class ConnectorImpl(Connector):
    def __init__(
        self,
        client: Client,
        locale: str = "en_US",
        currency: str = "USD",
        preferred_channel: str = "ecommerce",
        cache_file: Path = None,
        check: bool = True,
    ) -> None:
        self._cache_file = cache_file

        self._loaded: set[str] = set()

        if cache_file != None and cache_file.exists():
            self._cache = self._load_from_file()
            if client != self._cache.client:
                del self._cache
        if not hasattr(self, "_cache"):
            self._cache = Cache(client, locale, currency, preferred_channel)
            if check:
                self._cache.check()
            if cache_file != None:
                cache_file.touch()
                self._dump_to_file()

    # --------------------------------------------------------------------------

    @property
    def client(self) -> Client:
        return self._cache.client

    def get_attributes(self) -> list[models.Attribute]:
        return self._get_from_cache("attributes")

    def get_categories(self) -> list[models.Category]:
        return self._get_from_cache("categories")

    def get_families(self) -> list[models.Family]:
        return self._get_from_cache("families")

    def get_products(self) -> list[models.Product]:
        return self._get_from_cache("products")

    # --------------------------------------------------------------------------

    def _get_from_cache(self, attribute: str) -> list:
        result = self._cache.__getattribute__(attribute)
        if attribute not in self._loaded:
            self._dump_to_file()
            self._loaded.add(attribute)
        return result

    # --------------------------------------------------------------------------

    def _load_from_file(self) -> Cache | None:
        file = open(self._cache_file, "r+b")
        return pk.load(file)

    def _dump_to_file(self):
        if self._cache_file != None:
            file = open(self._cache_file, "w+b")
            pk.dump(self._cache, file)
