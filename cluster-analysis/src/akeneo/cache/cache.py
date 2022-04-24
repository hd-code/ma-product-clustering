from pathlib import Path

from .. import models
from ..client.client import Client
from .fetcher import Fetcher
from .files import Files
from .loader import Loader


class Cache:
    """Caches the data from akeneo

    Call `fetch_data_from_api` to query all endpoints and save the responses to
    the `data_dir`. Afterwards, the data can be accessed through the properties
    of this class.
    """
    def __init__(self, data_dir: Path, client: Client = None) -> None:
        self._data_dir = data_dir
        self._client = client

        self._loader = Loader(data_dir)

    # --------------------------------------------------------------------------

    def fetch_data_from_api(self) -> None:
        client = self._client
        if not client:
            raise ValueError("no Client provided")
        Fetcher(client, self._data_dir)

    # --------------------------------------------------------------------------

    @property
    def attribute_groups(self) -> list[models.AttributeGroup]:
        return self._loader.load(Files.ATTRIBUTE_GROUPS.value)

    @property
    def attributes(self) -> list[models.Attribute]:
        attr: list[models.Attribute] = self._loader.load(Files.ATTRIBUTES.value)
        return self._add_attribute_options(attr)

    @property
    def categories(self) -> list[models.Category]:
        return self._loader.load(Files.CATEGORIES.value)

    @property
    def channels(self) -> list[models.Channel]:
        return self._loader.load(Files.CHANNELS.value)

    @property
    def currencies(self) -> list[models.Currency]:
        return self._loader.load(Files.CURRENCIES.value)

    @property
    def families(self) -> list[models.Family]:
        return self._loader.load(Files.FAMILIES.value)

    @property
    def locales(self) -> list[models.Locale]:
        return self._loader.load(Files.LOCALES.value)

    @property
    def measurements(self) -> list[models.MeasurementFamily]:
        return self._loader.load(Files.MEASUREMENTS.value)

    @property
    def products(self) -> list[models.Product]:
        return self._loader.load(Files.PRODUCTS.value)

    # --------------------------------------------------------------------------

    def _add_attribute_options(
        self, attributes: list[models.Attribute]
    ) -> list[models.Attribute]:
        for i in range(len(attributes)):
            attr = attributes[i]
            if attr.type not in {
                models.AttributeType.SELECT_SINGLE,
                models.AttributeType.SELECT_MULTI,
            }:
                continue
            options = self._loader.load_attribute_options(attr.code)
            attributes[i].options = options
        return attributes
