from typing import Type

from .centroid import Centroid, Datapoint
from .inits import InitFunc, random_init
from .kmeans_single import kmeans_single


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
        kmeans_result = kmeans_single(dataset, centroid_cls, n_cluster, init, max_iter)
        for _ in range(n_init - 1):
            kmeans_next = kmeans_single(
                dataset, centroid_cls, n_cluster, init, max_iter
            )
            if kmeans_next.mean_distance < kmeans_result.mean_distance:
                kmeans_result = kmeans_next

        self._result = kmeans_result

    # --------------------------------------------------------------------------

    @property
    def error(self) -> float:
        return self._result.mean_distance

    @property
    def error_per_cluster(self) -> list[float]:
        return self._result.mean_distances

    @property
    def iterations(self) -> int:
        return self._result.iterations

    @property
    def result(self) -> list[int]:
        return self._result.result
