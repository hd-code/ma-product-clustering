from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from .datapoint import Datapoint
from .kmeans import KMeans


@dataclass
class Cluster:
    dataset: list[Datapoint]
    dataset_i: list[int]
    error: float

    @property
    def error_orig(self) -> float:
        return self._error_orig

    @property
    def num_of_entries(self) -> int:
        return len(self.dataset_i)

    def __post_init__(self):
        self._error_orig = self.error

    def splinter_off_better_cluster(self, do_kmeans: Callable[[list[Datapoint]], KMeans]) -> Cluster:
        kmeans = do_kmeans(self.dataset)
        dataset, dataset_i = self._get_separated_dataset(kmeans.result)

        errors = kmeans.error_per_cluster
        better_i, worse_i = (0, 1) if errors[0] < errors[1] else (1, 0)

        self.dataset = dataset[worse_i]
        self.dataset_i = dataset_i[worse_i]
        self.error = errors[worse_i]

        return Cluster(
            dataset[better_i],
            dataset_i[better_i],
            errors[better_i],
        )

    def _get_separated_dataset(self, cluster_result: list[int]) -> tuple[list[list[Datapoint]], list[list[int]]]:
        dataset: list[list[Datapoint]] = [[], []]
        dataset_i: list[list[int]] = [[], []]

        for i in range(self.num_of_entries):
            cluster_i = cluster_result[i]

            datapoint = self.dataset[i]
            datapoint_i = self.dataset_i[i]

            dataset[cluster_i].append(datapoint)
            dataset_i[cluster_i].append(datapoint_i)

        return dataset, dataset_i
