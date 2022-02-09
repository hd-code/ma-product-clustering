from typing import Type

from .centroid import Centroid, Datapoint
from .inits import InitFunc, random_init
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
    ) -> None:
        tries = [
            KMeansSingle(dataset, centroid_cls, n_cluster, init, max_iter)
            for _ in range(n_init)
        ]

        best_index = 0
        error = tries[0].error
        for i in range(1, n_init):
            next_error = tries[i].error
            if next_error < error:
                best_index = i
                error = next_error

        self._result = tries[best_index]

    # --------------------------------------------------------------------------

    @property
    def error(self) -> float:
        return self._result.error

    @property
    def error_per_cluster(self) -> list[float]:
        return self._result.error_per_cluster

    @property
    def iterations(self) -> int:
        return self._result.iterations

    @property
    def result(self) -> list[int]:
        return self._result.result
