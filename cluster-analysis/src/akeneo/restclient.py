import abc
from typing import Union

from akeneo.route import AkeneoRoute


JsonBody = Union[dict, list]


class AkeneoRestClient(abc.ABC):

    @property
    @abc.abstractmethod
    def routes(self) -> list[AkeneoRoute]:
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, route_id: str, path_vars: dict[str, str] = None, params: dict = None) -> JsonBody:
        raise NotImplementedError

    @abc.abstractmethod
    def get_list(self, route_id: str, path_vars: dict[str, str] = None, params: dict = None) -> list[dict]:
        raise NotImplementedError
