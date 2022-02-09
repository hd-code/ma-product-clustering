import abc
from typing import Union

from akeneo import models

JsonBody = Union[dict, list]


class Client(abc.ABC):
    """Rest client to access an Akeneo-PIM instance"""

    @abc.abstractmethod
    def get_routes(self) -> list[models.Route]:
        """Overview over the available endpoints"""
        raise NotImplementedError

    @abc.abstractmethod
    def get(
        self, route_id: str, path_vars: dict[str, str] = None, params: dict = None
    ) -> JsonBody:
        """GET request against one of the endpoints"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_list(
        self, route_id: str, path_vars: dict[str, str] = None, params: dict = None
    ) -> list[dict]:
        """GET request against a list endpoint removing pagination"""
        raise NotImplementedError
