from __future__ import annotations
from dataclasses import dataclass
import math
import random

from clustering.data_point_3d import DataPoint3DVector
from clustering.middle_point import MiddlePoint


@dataclass
class MiddlePoint3DVector(MiddlePoint):
    x: float
    y: float
    z: float
    n: int = 0

    @classmethod
    def create_points(cls, data: list[DataPoint3DVector], num_of_points: int) -> list[MiddlePoint3DVector]:
        indexes: set[int] = set()
        for num_of_indexes in range(num_of_points):
            while (len(indexes) <= num_of_indexes):
                index = random.randint(0, len(data) - 1)
                indexes.add(index)

        result: list[MiddlePoint3DVector] = []
        for index in list(indexes):
            data_point = data[index]
            middle_point = cls(data_point.x, data_point.y, data_point.z)
            result.append(middle_point)

        return result

    def calc_distance(self, data_point: DataPoint3DVector) -> float:
        result = math.pow(self.x - data_point.x, 2)
        result += math.pow(self.y - data_point.y, 2)
        result += math.pow(self.z - data_point.z, 2)
        return math.sqrt(result)

    def on_add_point(self, data_point: DataPoint3DVector) -> None:
        n_new = self.n + 1
        self.x = (self.x * self.n + data_point.x) / n_new
        self.y = (self.y * self.n + data_point.y) / n_new
        self.z = (self.z * self.n + data_point.z) / n_new
        self.n = n_new

    def on_restart(self) -> None:
        self.n = 0
