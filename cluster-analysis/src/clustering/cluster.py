from __future__ import annotations
from dataclasses import dataclass, field

from clustering.data_point import DataPoint
from clustering.middle_point import MiddlePoint


@dataclass
class Cluster:
    middle_point: MiddlePoint
    members: list[DataPoint] = field(default_factory=list)
    parent: Cluster = None

    def add_point(self, data_point: DataPoint):
        self.members.append(data_point)
        data_point.set_cluster(self)
        self.middle_point.on_add_point(data_point)

    def calc_distance(self, data_point: DataPoint) -> float:
        return self.middle_point.calc_distance(data_point)

    def restart(self):
        self.members = []
        self.middle_point.on_restart()
