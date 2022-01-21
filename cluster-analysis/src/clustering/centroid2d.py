from __future__ import annotations

from dataclasses import dataclass, field
from typing import Type

from .centroid import Centroid
from .datapoint2d import Datapoint2D


@dataclass
class Centroid2D(Centroid, Datapoint2D):
    n: int = 0
    next_mp: Datapoint2D = field(default_factory=lambda: Datapoint2D(0, 0))

    @classmethod
    def init_from_datapoint(cls: Type[Centroid2D], datapoint: Datapoint2D) -> Centroid2D:
        result = cls(datapoint.x, datapoint.y)
        result.on_add_point(datapoint)
        return result

    def calc_distance(self, datapoint: Datapoint2D) -> float:
        return datapoint.calc_distance(self)

    def on_add_point(self, datapoint: Datapoint2D) -> None:
        n_new = self.n + 1
        self.next_mp.x = (self.next_mp.x * self.n + datapoint.x) / n_new
        self.next_mp.y = (self.next_mp.y * self.n + datapoint.y) / n_new
        self.n = n_new

    def on_restart(self) -> None:
        self.x = self.next_mp.x
        self.y = self.next_mp.y

        self.next_mp = Datapoint2D(0, 0)
        self.n = 0
