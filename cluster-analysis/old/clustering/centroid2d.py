from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Type

from .centroid import Centroid


@dataclass
class Datapoint2D:
    x: float
    y: float


@dataclass
class Centroid2D(Centroid, Datapoint2D):
    n: int = 0
    next: Datapoint2D = field(default_factory=lambda: Datapoint2D(0, 0))

    @classmethod
    def init_from_datapoint(
        cls: Type[Centroid2D], datapoint: Datapoint2D
    ) -> Centroid2D:
        result = cls(datapoint.x, datapoint.y)
        result.on_add_point(datapoint)
        return result

    def calc_distance(self, datapoint: Datapoint2D) -> float:
        result = math.pow(self.x - datapoint.x, 2)
        result += math.pow(self.y - datapoint.y, 2)
        return math.sqrt(result)

    def on_add_point(self, datapoint: Datapoint2D) -> None:
        n_new = self.n + 1
        self.next.x = (self.next.x * self.n + datapoint.x) / n_new
        self.next.y = (self.next.y * self.n + datapoint.y) / n_new
        self.n = n_new

    def on_restart(self) -> None:
        self.x = self.next.x
        self.y = self.next.y

        self.next = Datapoint2D(0, 0)
        self.n = 0
