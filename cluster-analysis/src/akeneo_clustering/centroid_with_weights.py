from typing import Type

from src import clustering

from .centroid import Centroid
from .datapoint import Datapoint
from .distance import distance


def create_centroid_cls_with_weights(
    weights: dict[str, float]
) -> Type[clustering.Centroid]:
    class _CentroidWithWeights(CentroidWithWeights):
        @property
        def weights(self) -> dict[str, float]:
            return weights

    return _CentroidWithWeights


class CentroidWithWeights(Centroid):
    def calc_distance(self, datapoint: Datapoint) -> float:
        if self._has_changed:
            self._update_values()
        return distance(self._values, datapoint, self.weights)

    @property
    def weights(self) -> dict[str, float]:
        raise NotImplementedError
