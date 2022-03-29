from typing import Type

import numpy as np

from .centroid import Centroid, Datapoint
from .inits import InitFunc, random_init, seed_random_init
from .kmeans_single import KMeansSingle


class KMeans:
    """Clusters a dataset with KMeans"""

    def __init__(
        self,
        dataset: list[Datapoint],
        centroid_cls: Type[Centroid],
        n_cluster: int = 5,
        init: InitFunc = random_init,
        n_init: int = 10,
        max_iter: int = 100,
        random_state: int = None,
    ) -> None:
        if random_state != None:
            seed_random_init(random_state)

        kmeanses = [
            KMeansSingle(dataset, centroid_cls, n_cluster, init, max_iter)
            for _ in range(n_init)
        ]
        errors = [k.error for k in kmeanses]
        best_clustering_i = np.array(errors).argmin()
        self._result = kmeanses[best_clustering_i]

    # --------------------------------------------------------------------------

    @property
    def error(self) -> float:
        """Sum distance of all points to their cluster"""
        return self._result.error

    @property
    def error_per_cluster(self) -> np.ndarray:
        """Sum distance of all points to their cluster by cluster"""
        return self._result.error_per_cluster

    @property
    def iterations(self) -> int:
        """Number of iterations needed before the clusters converged"""
        return self._result._iterations

    @property
    def labels(self) -> np.ndarray:
        """IntVector(n x 1) that shows which datapoint belongs to which cluster"""
        return self._result.labels
