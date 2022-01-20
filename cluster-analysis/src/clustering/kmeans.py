from typing import Type

from .centroid import Centroid
from .datapoint import Datapoint
from .kmeans_single import KMeansSingle


class KMeans:
    """Clusters a dataset with KMeans"""

    def __init__(
        self,
        dataset: list[Datapoint],
        middle_point_cls: Type[Centroid],
        k: int = 5,
        max_iter: int = 100,
        num_of_trys: int = 1,
    ) -> None:
        tries: list[KMeansSingle] = []
        for i in range(num_of_trys):
            trial = KMeansSingle(dataset, middle_point_cls, k, max_iter)
            tries.append(trial)

        best_index = 0
        mean_distances = tries[0].mean_distances
        error = sum(mean_distances) / len(mean_distances)
        for i in range(1, num_of_trys):
            mean_distances = tries[i].mean_distances
            next_error = sum(mean_distances) / len(mean_distances)
            if next_error < error:
                best_index = i
                error = next_error

        self._result = tries[best_index]

    # --------------------------------------------------------------------------

    @property
    def iterations(self) -> int:
        return self._result.iterations

    @property
    def mean_distances(self) -> list[float]:
        return self._result.mean_distances

    @property
    def middle_points(self) -> list[Centroid]:
        return self._result.middle_points

    @property
    def result(self) -> list[int]:
        return self._result.result

    def predict(self, dataset: list[Datapoint]) -> list[int]:
        return self._result.predict(dataset)

    def predict_single(self, datapoint: Datapoint) -> int:
        return self._result.predict_single(datapoint)
