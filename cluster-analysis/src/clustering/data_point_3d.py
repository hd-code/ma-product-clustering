from dataclasses import dataclass

from clustering.cluster import Cluster
from clustering.data_point import DataPoint


@dataclass
class DataPoint3DVector(DataPoint):
    id: int
    x: float
    y: float
    z: float
    _cluster: Cluster = None

    def get_cluster(self) -> Cluster:
        return self._cluster

    def set_cluster(self, cluster: Cluster) -> None:
        self._cluster = cluster

    def get_id(self) -> int:
        return self.id
