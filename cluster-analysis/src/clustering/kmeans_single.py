from typing import Type

from .centroid import Centroid
from .datapoint import Datapoint
from .inits import InitFunc, random_init


class KMeansSingle:
    """Single run of k-means over the dataset

    The clustering starts immediately on instancing the class and may take some
    time to compute.
    """

    def __init__(
        self,
        dataset: list[Datapoint],
        centroid_cls: Type[Centroid],
        k: int = 5,
        init: InitFunc = random_init,
        max_iter: int = 100,
    ) -> None:
        self._dataset = dataset
        self._centroid_cls = centroid_cls
        self._num_of_clusters = k
        self._init = init
        self._max_iter = max_iter

        self._centroids: list[Centroid] = []
        self._dataset_to_cluster = [-1] * len(dataset)
        self._iterations = 0
        self._num_of_datapoints = len(dataset)

        self._cluster_dataset()

    # --------------------------------------------------------------------------

    @property
    def error(self) -> float:
        return sum(self.error_per_cluster)

    @property
    def error_per_cluster(self) -> list[float]:
        if not hasattr(self, "_error_per_cluster"):
            result = [0.0] * self._num_of_clusters
            for point_i in range(self._num_of_datapoints):
                datapoint = self._dataset[point_i]
                cluster_i = self._dataset_to_cluster[point_i]
                distance = self._centroids[cluster_i].calc_distance(datapoint)
                result[cluster_i] += distance * distance
            self._error_per_cluster = result
        return self._error_per_cluster

    @property
    def iterations(self) -> int:
        return self._iterations

    @property
    def result(self) -> list[int]:
        return self._dataset_to_cluster

    # --------------------------------------------------------------------------

    def _cluster_dataset(self):
        self._cluster_init()
        self._iterations += 1

        while self._iterations <= self._max_iter:
            have_clusters_changed = self._recluster()
            self._iterations += 1

            if not have_clusters_changed:
                break

    def _cluster_init(self):
        init_points_i = self._init(self._dataset, self._num_of_clusters)
        for init_point_i in init_points_i:
            datapoint = self._dataset[init_point_i]
            centroid = self._centroid_cls.init_from_datapoint(datapoint)

            self._dataset_to_cluster[init_point_i] = len(self._centroids)
            self._centroids.append(centroid)

        for point_i in range(self._num_of_datapoints):
            if point_i in init_points_i:
                continue

            datapoint = self._dataset[point_i]
            cluster_index = self._find_nearest_cluster(datapoint)

            self._dataset_to_cluster[point_i] = cluster_index
            self._centroids[cluster_index].on_add_point(datapoint)

    def _find_nearest_cluster(self, datapoint: Datapoint) -> int:
        result = 0
        distance = self._centroids[0].calc_distance(datapoint)
        for index in range(1, self._num_of_clusters):
            centroid = self._centroids[index]
            next_distance = centroid.calc_distance(datapoint)
            if next_distance < distance:
                distance = next_distance
                result = index
        return result

    def _recluster(self) -> bool:
        [c.on_restart() for c in self._centroids]
        have_clusters_changed = False
        for point_i in range(self._num_of_datapoints):
            datapoint = self._dataset[point_i]
            cluster_index = self._find_nearest_cluster(datapoint)
            if cluster_index != self._dataset_to_cluster[point_i]:
                have_clusters_changed = True
                self._dataset_to_cluster[point_i] = cluster_index
            self._centroids[cluster_index].on_add_point(datapoint)
        return have_clusters_changed
