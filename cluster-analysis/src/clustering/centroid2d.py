from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Type

from .centroid import Centroid


@dataclass
class Datapoint2D:
    x: float
    y: float


@dataclass
class Centroid2D(Centroid, Datapoint2D):
    n: int = 0

    @classmethod
    def init(cls: Type[Centroid2D]) -> Centroid2D:
        return cls(0, 0)

    def calc_distance(self, datapoint: Datapoint2D) -> float:
        result = math.pow(self.x - datapoint.x, 2)
        result += math.pow(self.y - datapoint.y, 2)
        return math.sqrt(result)

    def on_add_point(self, datapoint: Datapoint2D) -> None:
        n_new = self.n + 1
        self.x = (self.x * self.n + datapoint.x) / n_new
        self.y = (self.y * self.n + datapoint.y) / n_new
        self.n = n_new
