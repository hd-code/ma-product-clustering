from __future__ import annotations
from abc import ABC, abstractmethod


class DataPoint(ABC):
    @abstractmethod
    def calc_distance(self, data_point: DataPoint) -> float:
        raise NotImplementedError
