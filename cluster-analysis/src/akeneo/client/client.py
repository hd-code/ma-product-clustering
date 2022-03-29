import abc
from typing import Union

from .route import PathVars, Route

JsonBody = Union[dict, list]


class Client(abc.ABC):
    """Rest client to access an Akeneo-PIM instance"""

    @abc.abstractmethod
    def get_routes(self) -> list[Route]:
        """Overview over the available endpoints"""
        raise NotImplementedError

    @abc.abstractmethod
    def request(
        self,
        route_id: str,
        path_vars: PathVars = None,
        body: JsonBody = None,
        params: dict = None,
    ) -> JsonBody:
        """Send a request against an endpoint"""
        raise NotImplementedError
