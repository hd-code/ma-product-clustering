from __future__ import annotations
from abc import ABC, abstractmethod

from .data_point import DataPoint


class MiddlePoint(DataPoint, ABC):
    @classmethod
    @abstractmethod
    def create_points(cls, data: list[DataPoint], num_of_points: int) -> list[MiddlePoint]:
        raise NotImplementedError

    @abstractmethod
    def on_add_point(self, data_point: DataPoint) -> None:
        raise NotImplementedError

    @abstractmethod
    def on_restart(self) -> None:
        raise NotImplementedError
