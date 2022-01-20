from __future__ import annotations

from dataclasses import dataclass, field
from typing import Type

from .centroid import Centroid
from .datapoint2d import Datapoint2D
import util


@dataclass
class Centroid2D(Centroid, Datapoint2D):
    n: int = 0
    next_mp: Datapoint2D = field(default_factory=lambda: Datapoint2D(0, 0))

    @classmethod
    def create(cls: Type[Centroid2D], data: list[Datapoint2D], num_of_points: int) -> list[Centroid2D]:
        result: list[Centroid2D] = []
        for index in range(num_of_points):
            datapoint = data[index]
            middle_point = cls(datapoint.x, datapoint.y)
            result.append(middle_point)
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


@dataclass
class Centroid2DRandom(Centroid2D):

    @classmethod
    def create(cls: Type[Centroid2DRandom], data: list[Datapoint2D], num_of_points: int) -> list[Centroid2DRandom]:
        result: list[Centroid2DRandom] = []
        indexes = util.random_int_set(num_of_points, 0, len(data) - 1)
        for index in list(indexes):
            datapoint = data[index]
            middle_point = cls(datapoint.x, datapoint.y)
            result.append(middle_point)
        return result
