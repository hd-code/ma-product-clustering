from __future__ import annotations

from typing import Type

import numpy as np

from .centroid import Centroid, Datapoint
from .inits import InitFunc, random_init, seed_random_init
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
        centroid_cls: Type[Centroid],
        kmeans_init: InitFunc = random_init,
        kmeans_n_init: int = 10,
        kmeans_max_iter: int = 100,
        random_state: int = None,
    ) -> None:
        if random_state is not None:
            seed_random_init(random_state)

        self._dataset = np.array(dataset)
        self._dataset_to_cluster = [{0} for _ in range(len(dataset))]

        error_init = KMeans(dataset, centroid_cls, 1, lambda *_: {0}, 1).error

        self._cluster_splitted = np.array([-1])
        self._cluster_errors = np.array([error_init])
        self._cluster_errors_history = np.array([error_init])
        self._cluster_to_dataset_i = [np.array(range(len(dataset)))]

        self._kmeans = lambda dataset: KMeans(
            dataset,
            centroid_cls,
            2,
            kmeans_init,
            kmeans_n_init,
            kmeans_max_iter,
        )

        self._cluster_dataset()

    # --------------------------------------------------------------------------

    @property
    def dendrogram_matrix(self) -> np.ndarray:
        n_datapoints = len(self._dataset)

        result = np.array([[0.0, 0.0, 0.0, 0.0]])

        cluster_alias = {i: i for i in range(n_datapoints)}
        n_cluster = n_datapoints
        cluster_count = {i: 1 for i in range(n_datapoints)}

        for i in range(1, n_datapoints):
            merged_cluster = n_datapoints - i
            merged_points = np.array(self.labels_flat(merged_cluster))[
                np.array(self.labels_flat(merged_cluster + 1)) == merged_cluster
            ]
            merged_with = merged_points[0]

            cluster_count[merged_with] += len(merged_points)

            result = np.append(
                result,
                [
                    [
                        cluster_alias[merged_cluster],
                        cluster_alias[merged_with],
                        self._cluster_errors_history[merged_cluster],
                        cluster_count[merged_with],
                    ]
                ],
                axis=0,
            )

            cluster_alias[merged_with] = n_cluster
            n_cluster += 1
        return result[1:]

    @property
    def errors(self) -> np.ndarray:
        return self._cluster_errors_history

    @property
    def labels(self) -> list[set[int]]:
        return self._dataset_to_cluster

    def labels_flat(self, num_of_clusters: int = None) -> list[int]:
        """Returns the labels for a specific level in the cluster hierarchy"""
        if num_of_clusters is None:
            return [max(d) for d in self._dataset_to_cluster]

        return [
            max(filter(lambda c: c < num_of_clusters, d))  # type: ignore
            for d in self._dataset_to_cluster
        ]

    # --------------------------------------------------------------------------

    def _cluster_dataset(self):
        cluster_to_split = self._find_cluster_to_split()
        while cluster_to_split != -1:
            self._split_cluster(cluster_to_split)
            cluster_to_split = self._find_cluster_to_split()

    def _find_cluster_to_split(self) -> int:
        cluster_i = self._cluster_errors.argmax()
        if len(self._cluster_to_dataset_i[cluster_i]) > 1:
            return int(cluster_i)

        for i in range(cluster_i, len(self._cluster_errors)):
            if len(self._cluster_to_dataset_i[i]) > 1:
                return i

        return -1

    def _split_cluster(self, cluster_to_split: int) -> None:
        cluster_orig = cluster_to_split
        cluster_new = len(self._cluster_splitted)

        datapoints_i = self._cluster_to_dataset_i[cluster_orig]

        kmeans = self._kmeans(self._dataset[datapoints_i])
        errors = kmeans.error_per_cluster
        better_i, worse_i = (0, 1) if errors[0] < errors[1] else (1, 0)

        better_dpi = datapoints_i[np.array(kmeans.labels) == better_i]
        worse_dpi = datapoints_i[np.array(kmeans.labels) == worse_i]

        self._cluster_splitted = np.append(self._cluster_splitted, cluster_orig)

        self._cluster_errors[cluster_orig] = errors[worse_i]
        self._cluster_errors = np.append(self._cluster_errors, errors[better_i])

        self._cluster_errors_history = np.append(
            self._cluster_errors_history, self._cluster_errors.mean()
        )

        self._cluster_to_dataset_i[cluster_orig] = worse_dpi
        self._cluster_to_dataset_i.append(better_dpi)

        [self._dataset_to_cluster[i].add(cluster_new) for i in better_dpi]
