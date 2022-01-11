from __future__ import annotations
from dataclasses import dataclass

from clustering.data_point_3d import DataPoint3D
from clustering.middle_point import MiddlePoint


@dataclass
class MiddlePoint3D(MiddlePoint, DataPoint3D):
    n: int = 0

    @classmethod
    def create_points(cls, data: list[DataPoint3D], num_of_points: int) -> list[MiddlePoint3D]:
        result: list[MiddlePoint3D] = []
        for index in range(num_of_points):
            data_point = data[index]
            middle_point = cls(data_point.x, data_point.y, data_point.z)
            result.append(middle_point)
        return result

    def on_add_point(self, data_point: DataPoint3D) -> None:
        n_new = self.n + 1
        self.x = (self.x * self.n + data_point.x) / n_new
        self.y = (self.y * self.n + data_point.y) / n_new
        self.z = (self.z * self.n + data_point.z) / n_new
        self.n = n_new

    def on_restart(self) -> None:
        self.n = 0
