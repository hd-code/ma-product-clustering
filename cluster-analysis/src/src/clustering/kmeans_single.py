from typing import Type

import numpy as np

from .centroid import Centroid, Datapoint
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
        n_cluster: int = 5,
        init: InitFunc = random_init,
        max_iter: int = 100,
    ) -> None:
        self._dataset = dataset
        self._centroid_cls = centroid_cls
        self._n_cluster = n_cluster
        self._init = init
        self._max_iter = max_iter

        self._centroids = self._init_centroids()
        self._iterations = 0
        self._result = np.zeros(len(dataset), dtype=int)

        self._cluster_dataset()

    # --------------------------------------------------------------------------

    @property
    def centroids(self) -> list[Centroid]:
        return self._centroids

    @property
    def error(self) -> float:
        return self.error_per_cluster.mean()

    @property
    def error_per_cluster(self) -> np.ndarray:
        if not hasattr(self, "_error_per_cluster"):
            sum = [0.0 for _ in range(self._n_cluster)]
            n = [0 for _ in range(self._n_cluster)]
            for i in range(len(self._dataset)):
                datapoint = self._dataset[i]
                cluster_i = self._result[i]

                sum[cluster_i] += self._centroids[cluster_i].calc_distance(datapoint)
                n[cluster_i] += 1
            self._error_per_cluster = np.array(sum) / np.array(n)
        return self._error_per_cluster

    @property
    def iterations(self) -> int:
        return self._iterations

    @property
    def result(self) -> np.ndarray:
        return self._result

    # --------------------------------------------------------------------------

    def _init_centroids(self) -> list[Centroid]:
        result: list[Centroid] = []
        startpoints_i = self._init(self._dataset, self._n_cluster)
        for i in startpoints_i:
            centroid = self._centroid_cls.init()
            centroid.on_add_point(self._dataset[i])
            result.append(centroid)
        return result

    def _re_init_centroids(self) -> list[Centroid]:
        result = [self._centroid_cls.init() for _ in range(self._n_cluster)]
        for i in range(len(self._dataset)):
            datapoint = self._dataset[i]
            result[self._result[i]].on_add_point(datapoint)
        return result

    def _cluster_dataset(self):
        has_changed = True
        while has_changed and self._iterations < self._max_iter:
            has_changed = self._assign_points()
            self._iterations += 1
            if has_changed:
                self._centroids = self._re_init_centroids()

    def _assign_points(self) -> bool:
        has_changed = False
        for i in range(len(self._dataset)):
            datapoint = self._dataset[i]
            cluster_i = self._find_nearest_cluster(datapoint)
            if cluster_i != self._result[i]:
                has_changed = True
                self._result[i] = cluster_i
        return has_changed

    def _find_nearest_cluster(self, datapoint: Datapoint) -> int:
        result = -1
        distance = float("inf")
        for i in range(self._n_cluster):
            dist_to_cluster = self._centroids[i].calc_distance(datapoint)
            if dist_to_cluster < distance:
                distance = dist_to_cluster
                result = i
        return result
