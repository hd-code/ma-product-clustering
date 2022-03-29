from typing import Type

import numpy as np

from .centroid import Centroid, Datapoint
from .inits import InitFunc, random_init, seed_random_init


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
        random_state: int = None,
    ) -> None:
        if random_state is not None:
            seed_random_init(random_state)

        self._dataset = dataset
        self._centroid_cls = centroid_cls
        self._n_cluster = n_cluster
        self._init = init
        self._max_iter = max_iter

        self._labels = np.zeros(len(dataset), dtype=int)
        self._iterations = 0

        self._init_centroids()
        self._cluster_dataset()

    # --------------------------------------------------------------------------

    @property
    def error(self) -> float:
        result = 0.0
        for i in range(len(self._dataset)):
            datapoint = self._dataset[i]
            cluster_i = self._labels[i]
            result += self._centroids[cluster_i].calc_distance(datapoint)
        return result

    @property
    def error_per_cluster(self) -> np.ndarray:
        result = np.zeros(self._n_cluster)
        for i in range(len(self._dataset)):
            datapoint = self._dataset[i]
            cluster_i = self._labels[i]
            result[cluster_i] += self._centroids[cluster_i].calc_distance(datapoint)
        return result

    @property
    def iterations(self) -> int:
        return self._iterations

    @property
    def labels(self) -> np.ndarray:
        return self._labels

    # --------------------------------------------------------------------------

    def _init_centroids(self):
        self._centroids: list[Centroid] = []
        startpoints_i = list(self._init(self._dataset, self._n_cluster))
        for i in startpoints_i:
            centroid = self._centroid_cls.init()
            centroid.on_add_point(self._dataset[i])
            self._labels[i] = len(self._centroids)
            self._centroids.append(centroid)

    def _re_init_centroids(self):
        self._centroids = [self._centroid_cls.init() for _ in range(self._n_cluster)]
        for i in range(len(self._dataset)):
            datapoint = self._dataset[i]
            self._centroids[self._labels[i]].on_add_point(datapoint)

    def _cluster_dataset(self):
        has_changed = True
        while has_changed and self._iterations < self._max_iter:
            has_changed = self._assign_points()
            self._iterations += 1
            if has_changed:
                self._re_init_centroids()

    def _assign_points(self) -> bool:
        has_changed = False
        for i in range(len(self._dataset)):
            datapoint = self._dataset[i]
            cluster_i = self._find_nearest_cluster(datapoint, self._labels[i])
            if cluster_i != self._labels[i]:
                has_changed = True
                self._labels[i] = cluster_i
        return has_changed

    def _find_nearest_cluster(
        self, datapoint: Datapoint, current_cluster_i: int = 0
    ) -> int:
        result = current_cluster_i
        distance = self._centroids[current_cluster_i].calc_distance(datapoint)
        for i in range(self._n_cluster):
            if i == current_cluster_i:
                continue
            dist_to_cluster = self._centroids[i].calc_distance(datapoint)
            if dist_to_cluster < distance:
                distance = dist_to_cluster
                result = i
        return result
