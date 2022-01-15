from .data_point import DataPoint
from .middle_point import MiddlePoint


class KMeans:
    def __init__(
        self,
        data_points: list[DataPoint],
        middle_point_cls: MiddlePoint,
        k: int = 5,
        max_iter: int = 100,
        num_of_trys: int = 1,
    ) -> None:
        self._assign(data_points, middle_point_cls, k, max_iter, num_of_trys)
        self._create_middle_points()
        self._init_rest()
        self._cluster_data()

    # public -------------------------------------------------------------------

    @property
    def iterations(self) -> int:
        return self._iterations

    @property
    def middle_points(self) -> list[MiddlePoint]:
        return self._middle_points

    @property
    def result(self) -> list[int]:
        return self._result

    def predict(self, data_points: list[DataPoint]) -> list[int]:
        return self._find_nearest_clusters(data_points)

    def predict_single(self, data_point: DataPoint) -> int:
        return self._find_nearest_cluster(data_point)

    # init ---------------------------------------------------------------------

    def _assign(
        self,
        data_points: list[DataPoint],
        middle_point_cls: MiddlePoint,
        k: int = 5,
        max_iter: int = 100,
        num_of_trys: int = 1,
    ) -> None:
        self._data_points = data_points
        self._middle_point_cls = middle_point_cls
        self._k = k
        self._num_of_trys = num_of_trys
        self._max_iter = max_iter

    def _create_middle_points(self) -> None:
        self._middle_points = self._middle_point_cls.create_points(
            self._data_points, self._k)

    def _init_rest(self) -> None:
        self._iterations = 0
        self._result: list[int] = []

    # clustering ---------------------------------------------------------------

    def _cluster_data(self) -> None:
        self._init_clustering()
        self._iterations += 1

        while self.iterations <= self._max_iter:
            have_clusters_changed = self._recluster()
            self._iterations += 1

            if not have_clusters_changed:
                break

    def _init_clustering(self) -> None:
        for i in range(len(self._data_points)):
            data_point = self._data_points[i]
            cluster_index = self._find_nearest_cluster(data_point)
            self._middle_points[cluster_index].on_add_point(data_point)
            self._result.append(cluster_index)

    def _recluster(self) -> bool:
        self._restart_middle_points()
        have_clusters_changed = False
        for i in range(len(self._data_points)):
            data_point = self._data_points[i]
            cluster_index = self._find_nearest_cluster(data_point)
            if cluster_index != self._result[i]:
                have_clusters_changed = True
                self._result[i] = cluster_index
            self._middle_points[cluster_index].on_add_point(data_point)
        return have_clusters_changed

    def _find_nearest_clusters(self, data_points: list[DataPoint]) -> list[int]:
        result: list[int] = []
        for data_point in data_points:
            cluster_index = self._find_nearest_cluster(data_point)
            result.append(cluster_index)
        return result

    def _find_nearest_cluster(self, data_point: DataPoint) -> int:
        result = 0
        distance = self._middle_points[0].calc_distance(data_point)
        for i in range(1, self._k):
            middle_point = self._middle_points[i]
            next_distance = middle_point.calc_distance(data_point)
            if next_distance < distance:
                distance = next_distance
                result = i
        return result

    def _restart_middle_points(self) -> None:
        for middle_point in self.middle_points:
            middle_point.on_restart()
