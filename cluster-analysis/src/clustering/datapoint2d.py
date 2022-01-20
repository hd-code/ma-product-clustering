from __future__ import annotations

from dataclasses import dataclass
import math

from .datapoint import Datapoint


@dataclass
class Datapoint2D(Datapoint):
    x: float
    y: float

    def calc_distance(self, datapoint: Datapoint2D) -> float:
        result = math.pow(self.x - datapoint.x, 2)
        result += math.pow(self.y - datapoint.y, 2)
        return math.sqrt(result)
