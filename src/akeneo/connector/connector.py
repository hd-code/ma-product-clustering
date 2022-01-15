from abc import ABC, abstractmethod

import akeneo.models as models


class Connector(ABC):

    @abstractmethod
    def get_attributes(self) -> list[models.Attribute]:
        raise NotImplementedError

    @abstractmethod
    def get_categories(self) -> list[models.Category]:
        raise NotImplementedError

    @abstractmethod
    def get_families(self) -> list[models.Family]:
        raise NotImplementedError

    @abstractmethod
    def get_products(self) -> list[models.Product]:
        raise NotImplementedError
