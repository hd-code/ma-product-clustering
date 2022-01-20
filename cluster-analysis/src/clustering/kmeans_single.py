from typing import Type

from .centroid import Centroid
from .datapoint import Datapoint


class KMeansSingle:
    """Single run of KMeans over the dataset
    
    The clustering starts immediately on instancing the class and may take some
    time to compute.
    """

    def __init__(
        self,
        dataset: list[Datapoint],
        middle_point_cls: Type[Centroid],
        k: int = 5,
        max_iter: int = 100,
    ) -> None:
        self._dataset = dataset
        self._num_of_clusters = k
        self._max_iter = max_iter

        self._iterations = 0
        self._middle_points = middle_point_cls.create(dataset, k)
        self._dataset_to_cluster: list[int] = [-1] * len(dataset)

        self._cluster_dataset()

    # --------------------------------------------------------------------------

    @property
    def iterations(self) -> int:
        return self._iterations

    @property
    def mean_distances(self) -> list[float]:
        if not hasattr(self, "_mean_distances"):
            result = [0.0] * self._num_of_clusters
            len_of_clusters = [0] * self._num_of_clusters

            for index in range(len(self._dataset)):
                datapoint = self._dataset[index]
                cluster_index = self._dataset_to_cluster[index]
                middle_point = self._middle_points[cluster_index]

                len_of_clusters[cluster_index] += 1
                result[cluster_index] += middle_point.calc_distance(datapoint)

            for index in range(self._num_of_clusters):
                result[index] = result[index] / len_of_clusters[index]

            self._mean_distances = result
        return self._mean_distances

    @property
    def middle_points(self) -> list[Centroid]:
        return self._middle_points

    @property
    def result(self) -> list[int]:
        return self._dataset_to_cluster

    def predict(self, dataset: list[Datapoint]) -> list[int]:
        return self._find_nearest_clusters(dataset)

    def predict_single(self, datapoint: Datapoint) -> int:
        return self._find_nearest_cluster(datapoint)

    # --------------------------------------------------------------------------

    def _cluster_dataset(self) -> None:
        self._init_clustering()
        self._iterations += 1

        while self._iterations <= self._max_iter:
            have_clusters_changed = self._recluster()
            self._iterations += 1

            if not have_clusters_changed:
                break

    def _init_clustering(self) -> None:
        for index in range(len(self._dataset)):
            datapoint = self._dataset[index]
            cluster_index = self._find_nearest_cluster(datapoint)

            self._middle_points[cluster_index].on_add_point(datapoint)
            self._dataset_to_cluster[index] = cluster_index

    def _recluster(self) -> bool:
        self._restart_middle_points()
        have_clusters_changed = False
        for index in range(len(self._dataset)):
            datapoint = self._dataset[index]
            cluster_index = self._find_nearest_cluster(datapoint)
            if cluster_index != self._dataset_to_cluster[index]:
                have_clusters_changed = True
                self._dataset_to_cluster[index] = cluster_index
            self._middle_points[cluster_index].on_add_point(datapoint)
        return have_clusters_changed

    def _find_nearest_clusters(self, dataset: list[Datapoint]) -> list[int]:
        result: list[int] = []
        for datapoint in dataset:
            cluster_index = self._find_nearest_cluster(datapoint)
            result.append(cluster_index)
        return result

    def _find_nearest_cluster(self, datapoint: Datapoint) -> int:
        result = 0
        distance = self._middle_points[0].calc_distance(datapoint)
        for index in range(1, self._num_of_clusters):
            middle_point = self._middle_points[index]
            next_distance = middle_point.calc_distance(datapoint)
            if next_distance < distance:
                distance = next_distance
                result = index
        return result

    def _restart_middle_points(self) -> None:
        for middle_point in self._middle_points:
            middle_point.on_restart()
