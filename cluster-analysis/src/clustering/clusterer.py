from clustering.cluster import Cluster
from clustering.data_point import DataPoint
from clustering.middle_point import MiddlePoint


class Clusterer:
    def __init__(self, middle_point_cls: MiddlePoint):
        self.create_middle_points = middle_point_cls.create_points

    def cluster_bisecting_k_means(self, data: list[DataPoint]) -> list[Cluster]:
        pass

    def cluster_k_mean(self, data: list[DataPoint], k: int) -> list[Cluster]:
        middle_points = self.create_middle_points(data, k)
        clusters = [Cluster(middle_point) for middle_point in middle_points]
        Clusterer.cluster_points(data, clusters)

    @staticmethod
    def cluster_points(data: list[DataPoint], clusters: list[Cluster]):
        num_of_clusters = len(clusters)
        for data_point in data:
            nearest_cluster = clusters[0]
            distance = nearest_cluster.calc_distance(data_point)
            for i in range(1, num_of_clusters):
                next_distance = clusters[i].calc_distance(data_point)
                if next_distance < distance:
                    distance = next_distance
                    nearest_cluster = clusters[i]
            nearest_cluster.add_point(data_point)
