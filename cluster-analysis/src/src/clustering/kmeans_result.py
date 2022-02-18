from dataclasses import dataclass, field

from .centroid import Centroid, Datapoint


@dataclass
class KMeansResult:
    dataset: list[Datapoint]
    result: list[int]
    centroids: list[Centroid]
    iterations: int
    mean_distances: list[float] = field(init=False)
    mean_distance: float = field(init=False)

    def __post_init__(self) -> None:
        self._calc_mean_distances()
        self._calc_mean_distance()

    def _calc_mean_distances(self) -> None:
        distances = [0.0] * len(self.centroids)
        counts = [0] * len(self.centroids)

        for datapoint_i in range(len(self.result)):
            datapoint = self.dataset[datapoint_i]
            cluster_i = self.result[datapoint_i]

            distances[cluster_i] += self.centroids[cluster_i].calc_distance(datapoint)
            counts[cluster_i] += 1

        for i in range(len(counts)):
            distances[i] /= counts[i]

        self.mean_distances = distances

    def _calc_mean_distance(self) -> None:
        self.mean_distance = sum(self.mean_distances) / len(self.mean_distances)
