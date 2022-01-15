import abc
from typing import Union

import akeneo.models as models


JsonBody = Union[dict, list]


class Client(abc.ABC):

    @abc.abstractmethod
    def get_routes(self) -> list[models.Route]:
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, route_id: str, path_vars: dict[str, str] = None, params: dict = None) -> JsonBody:
        raise NotImplementedError

    @abc.abstractmethod
    def get_list(self, route_id: str, path_vars: dict[str, str] = None, params: dict = None) -> list[dict]:
        raise NotImplementedError
