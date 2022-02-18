from typing import Type

from .centroid import Centroid, Datapoint
from .inits import InitFunc, random_init
from .kmeans_result import KMeansResult


def init_centroids(
    dataset: list[Datapoint],
    centroid_cls: Type[Centroid],
    k: int,
    init: InitFunc,
) -> list[Centroid]:
    centroids: list[Centroid] = []

    init_indices = init(dataset, k)
    for index in init_indices:
        centroid = centroid_cls.init()
        centroid.on_add_point(dataset[index])
        centroids.append(centroid)

    return centroids


def re_init_centroids(
    dataset: list[Datapoint],
    map_datapoint_to_cluster: list[int],
    centroid_cls: Type[Centroid],
    k: int,
) -> list[Centroid]:
    centroids: list[Centroid] = [centroid_cls.init() for _ in range(k)]

    for datapoint_i in range(len(map_datapoint_to_cluster)):
        datapoint = dataset[datapoint_i]
        cluster_i = map_datapoint_to_cluster[datapoint_i]
        centroids[cluster_i].on_add_point(datapoint)

    return centroids


def find_closest_cluster(datapoint: Datapoint, centroids: list[Centroid]) -> int:
    result = 0
    distance = centroids[0].calc_distance(datapoint)

    for index in range(1, len(centroids)):
        next_distance = centroids[index].calc_distance(datapoint)
        if next_distance < distance:
            distance = next_distance
            result = index

    return result


def kmeans_single(
    dataset: list[Datapoint],
    centroid_cls: Type[Centroid],
    k: int = 5,
    init: InitFunc = random_init,
    max_iter: int = 100,
) -> KMeansResult:
    centroids = init_centroids(dataset, centroid_cls, k, init)

    result = [-1] * len(dataset)

    clusters_changed = True
    iterations = 0

    while clusters_changed and iterations < max_iter:
        clusters_changed = False

        for datapoint_i in range(len(dataset)):
            datapoint = dataset[datapoint_i]
            cluster_i = find_closest_cluster(datapoint, centroids)

            if result[datapoint_i] != cluster_i:
                result[datapoint_i] = cluster_i
                clusters_changed = True

        centroids = re_init_centroids(dataset, result, centroid_cls, k)

        iterations += 1

    return KMeansResult(dataset, result, centroids, iterations)
