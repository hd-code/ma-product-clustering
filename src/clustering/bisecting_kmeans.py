from __future__ import annotations
from dataclasses import Field, dataclass

from .data_point import DataPoint
from .kmeans import KMeans
from .middle_point import MiddlePoint


class BisectingKMeans:
    def __init__(
        self,
        data_points: list[DataPoint],
        middle_point_cls: MiddlePoint,
        kmeans_max_iter: int = 100,
        kmeans_num_of_trys: int = 1,
    ) -> None:
        self._assign(data_points, middle_point_cls,
                     kmeans_max_iter, kmeans_num_of_trys)

    # public -------------------------------------------------------------------

    # init ---------------------------------------------------------------------

    def _assign(
        self,
        data_points: list[DataPoint],
        middle_point_cls: MiddlePoint,
        kmeans_max_iter: int = 100,
        kmeans_num_of_trys: int = 1,
    ) -> None:
        self._data_points = data_points
        self._middle_point_cls = middle_point_cls
        self._kmeans_max_iter = kmeans_max_iter
        self._kmeans_num_of_trys = kmeans_num_of_trys

    def _init_attributes(self) -> None:
        self._result: list[int] = []
        self._clusters: list[int | None] = []

    # clustering ---------------------------------------------------------------

    def _cluster_data(self) -> None:
        pass

    def _bisect_data(self, data_points: list[DataPoint], data_points_index: list[int], parent_cluster_index: int):
        kmeans = KMeans(data_points, self._middle_point_cls, 2,
                        self._kmeans_max_iter, self._kmeans_num_of_trys)

        next_cluster_index = len(self._clusters)
        self._clusters.append(parent_cluster_index)
        self._clusters.append(parent_cluster_index)

        for i in len(range(kmeans.result)):
            # data_point = data_points[i]
            data_point_index = data_points_index[i]
            self._result[data_point_index] = next_cluster_index + \
                kmeans.result[i]
        pass


@dataclass
class Cluster:
    members: list[DataPoint] = Field(default_factory=list)
    members_index: list[int] = Field(default_factory=list)
    children: list[Cluster] = Field(default_factory=list)
    parent: Cluster | None = None
