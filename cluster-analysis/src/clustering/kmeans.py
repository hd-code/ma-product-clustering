import math
from typing import Callable

from clustering.data_point import DataPoint
from clustering.middle_point import MiddlePoint


def _on_cluster_found_noop(data_point_index: int, cluster_index: int) -> None:
    """Callback during clustering to perform some task when the nearest cluster for a point ist found"""
    pass


class KMeans:
    def __init__(
        self,
        middle_point_cls: MiddlePoint,
        k: int = 5,
        num_of_trys: int = 10,
        max_iter: int = 100,
    ) -> None:
        self._middle_point_cls = middle_point_cls
        self._k = k
        self._num_of_trys = num_of_trys
        self._max_iter = max_iter

    iterations = 0

    # public -------------------------------------------------------------------

    def fit(self, data: list[DataPoint]) -> list[int]:
        return self._cluster_data(data)

    def predict(self, data: list[DataPoint]) -> list[int]:
        self._check_is_initialized()
        return self._find_nearest_clusters(data)

    def predict_single(self, data_point: DataPoint) -> int:
        self._check_is_initialized()
        return self._find_nearest_cluster(data_point)

    # attributes ---------------------------------------------------------------

    def _create_middle_points(self, data: list[DataPoint]) -> None:
        self.middle_points = self._middle_point_cls.create_points(data, self._k)

    def _restart_middle_points(self) -> None:
        for middle_point in self.middle_points:
            middle_point.on_restart()

    def _check_is_initialized(self) -> None:
        if self.iterations == 0 or not hasattr(self, "middle_points"):
            print("Clustering not initialized. Use `fit` first.")
            raise AttributeError

    # clustering ---------------------------------------------------------------

    def _cluster_data(self, data: list[DataPoint]) -> list[int]:
        cluster_assigns = self._init_clustering(data)
        self.iterations += 1

        self._clusters_changed = False

        def on_cluster_found(data_point_index: int, cluster_index: int) -> None:
            data_point = data[data_point_index]
            middle_point = self.middle_points[cluster_index]
            middle_point.on_add_point(data_point)

            if cluster_assigns[data_point_index] != cluster_index:
                self._clusters_changed = True

        while self.iterations <= self._max_iter:
            self._clusters_changed = False
            self._restart_middle_points()

            cluster_assigns = self._find_nearest_clusters(
                data, on_cluster_found)
            self.iterations += 1

            if not self._clusters_changed:
                break

        return cluster_assigns

    def _init_clustering(self, data: list[DataPoint]) -> list[int]:
        self._create_middle_points(data)

        def update_mp(data_point_index: int, cluster_index: int) -> None:
            data_point = data[data_point_index]
            middle_point = self.middle_points[cluster_index]
            middle_point.on_add_point(data_point)

        return self._find_nearest_clusters(data, update_mp)

    def _find_nearest_clusters(
        self,
        data: list[DataPoint],
        on_cluster_found: Callable[[int, int], None] = _on_cluster_found_noop
    ) -> list[int]:
        result: list[int] = []
        for i in range(len(data)):
            data_point = data[i]
            cluster_index = self._find_nearest_cluster(data_point)
            on_cluster_found(i, cluster_index)
            result.append(cluster_index)
        return result

    def _find_nearest_cluster(self, data_point: DataPoint) -> int:
        result = 0
        distance = math.inf
        for i in range(self._k):
            middle_point = self.middle_points[i]
            next_distance = middle_point.calc_distance(data_point)
            if next_distance < distance:
                distance = next_distance
                result = i
        return result
