from abc import ABC, abstractmethod

from akeneo.models.attribute import AkeneoAttribute
from akeneo.models.category import AkeneoCategory
from akeneo.models.family import AkeneoFamily
from akeneo.models.product import AkeneoProduct, AkeneoProductValues


class AkeneoConnector(ABC):

    @abstractmethod
    def get_attributes(self) -> list[AkeneoAttribute]:
        raise NotImplementedError

    @abstractmethod
    def get_categories(self) -> list[AkeneoCategory]:
        raise NotImplementedError

    @abstractmethod
    def get_families(self) -> list[AkeneoFamily]:
        raise NotImplementedError

    @abstractmethod
    def get_products(self) -> list[AkeneoProduct]:
        raise NotImplementedError
