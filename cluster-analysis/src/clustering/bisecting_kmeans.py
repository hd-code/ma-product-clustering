from __future__ import annotations

from typing import Type

from .centroid import Centroid
from .cluster import Cluster
from .datapoint import Datapoint
from .inits import InitFunc, random_init
from .kmeans import KMeans


class BisectingKMeans:
    """Divisive clustering by repetitively splitting groups with `KMeans`

    The clustering starts immediately upon initializing the class and might take
    a while to compute.

    The `Datapoint` and `Centroid` interfaces have to be implemented by the
    passed data in order to work.
    """

    def __init__(
        self,
        dataset: list[Datapoint],
        middle_point_cls: Type[Centroid],
        kmeans_init: InitFunc = random_init,
        kmeans_n_init: int = 10,
        kmeans_max_iter: int = 100,
    ) -> None:
        self._dataset = dataset

        def kmeans(dataset: list[Datapoint]):
            return KMeans(dataset, middle_point_cls, 2,
                          kmeans_init, kmeans_n_init, kmeans_max_iter)
        self._kmeans = kmeans

        self._dataset_to_cluster: list[list[int]] = [
            [0]
            for _ in range(len(dataset))
        ]

        self._clusters: list[Cluster] = [
            Cluster(
                dataset,
                list(range(0, len(dataset))),
                KMeans(dataset, middle_point_cls, 1, lambda *_: [0], 1).error
            )
        ]

        self._cluster_dataset()

    # --------------------------------------------------------------------------

    @property
    def dataset(self) -> list[Datapoint]:
        return self._dataset

    @property
    def result(self) -> list[list[int]]:
        return self._dataset_to_cluster

    def result_flat(self, num_of_clusters: int = None) -> list[int]:
        if num_of_clusters == None:
            return [
                max(d)
                for d in self._dataset_to_cluster
            ]
        return [
            max(filter(lambda c: c < num_of_clusters, d))
            for d in self._dataset_to_cluster
        ]

    # --------------------------------------------------------------------------

    def _cluster_dataset(self):
        biggest_cluster_i = self._get_biggest_cluster_i()
        while biggest_cluster_i != -1:
            cluster = self._clusters[biggest_cluster_i]

            new_cluster = cluster.splinter_off_better_cluster(self._kmeans)
            new_cluster_i = len(self._clusters)

            self._clusters.append(new_cluster)
            for i in new_cluster.dataset_i:
                self._dataset_to_cluster[i].append(new_cluster_i)

            biggest_cluster_i = self._get_biggest_cluster_i()

    def _get_biggest_cluster_i(self) -> int:
        index = -1
        error = -float('inf')
        for i in range(len(self._clusters)):
            cluster = self._clusters[i]
            if cluster.num_of_entries > 1 and cluster.error > error:
                index = i
                error = cluster.error
        return index
