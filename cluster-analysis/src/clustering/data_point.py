from abc import ABC, abstractmethod
from typing import TypeVar


Cluster = TypeVar("Cluster")
Id = TypeVar("Id")


class DataPoint(ABC):
    @abstractmethod
    def get_cluster(self) -> Cluster:
        raise NotImplementedError

    @abstractmethod
    def set_cluster(self, cluster: Cluster) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_id(self) -> Id:
        raise NotImplementedError
