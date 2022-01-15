from __future__ import annotations
from dataclasses import dataclass
import math

from .data_point import DataPoint


@dataclass
class DataPoint3D(DataPoint):
    x: float
    y: float
    z: float

    def calc_distance(self, data_point: DataPoint3D) -> float:
        result = math.pow(self.x - data_point.x, 2)
        result += math.pow(self.y - data_point.y, 2)
        result += math.pow(self.z - data_point.z, 2)
        return math.sqrt(result)
