import unittest

from clustering.data_point_3d import DataPoint3D
from clustering.kmeans import KMeans
from clustering.middle_point_3d import MiddlePoint3D


class Test_KMeans(unittest.TestCase):
    def test_cluster_two_points_and_clusters(self):
        points = [
            DataPoint3D(1, 1, 1),
            DataPoint3D(2, 2, 2),
        ]

        kmeans = KMeans(points, MiddlePoint3D, 2)

        self.assertListEqual(kmeans.result, [0, 1])
        self.assertEqual(kmeans.iterations, 2,
                         "Should converge after second iteration")

    def test_cluster_four_points_and_clusters(self):
        points = [
            DataPoint3D(1, 1, 1),
            DataPoint3D(2, 2, 2),
            DataPoint3D(3, 3, 3),
            DataPoint3D(4, 4, 4),
        ]

        kmeans = KMeans(points, MiddlePoint3D, 4)

        self.assertListEqual(kmeans.result, [0, 1, 2, 3])
        self.assertEqual(kmeans.iterations, 2,
                         "Should converge after second iteration")

    def test_cluster_several_points_suboptimal_start(self):
        points = [
            DataPoint3D(1, 1, 1),
            DataPoint3D(1, 2, 1),
            DataPoint3D(2, 2, 2),
            DataPoint3D(2, 2, 4),
            DataPoint3D(3, 3, 3),
            DataPoint3D(4, 4, 4),
            DataPoint3D(11, 1, 1),
            DataPoint3D(11, 2, 1),
            DataPoint3D(12, 2, 2),
            DataPoint3D(12, 2, 4),
            DataPoint3D(13, 3, 3),
            DataPoint3D(14, 4, 4),
        ]

        kmeans = KMeans(points, MiddlePoint3D, 3)

        self.assertListEqual(kmeans.result, [0, 0, 0, 1, 1, 1, 2, 2, 2, 2, 2, 2])
        self.assertEqual(kmeans.iterations, 5)

    def test_cluster_with_wild_ordering(self):
        points = [
            DataPoint3D(11, 1, 1),
            DataPoint3D(3, 3, 0),
            DataPoint3D(11, 2, 1),
            DataPoint3D(1, 1, 1),
            DataPoint3D(2, 12, 4),
            DataPoint3D(2, 2, 0),
            DataPoint3D(4, 4, 0),
            DataPoint3D(1, 2, 1),
            DataPoint3D(4, 14, 4),
            DataPoint3D(12, 2, 2),
            DataPoint3D(2, 2, 2),
            DataPoint3D(3, 13, 3),
        ]

        kmeans = KMeans(points, MiddlePoint3D, 4)

        self.assertListEqual(kmeans.result, [0, 3, 2, 3, 1, 3, 3, 3, 1, 2, 3, 1])
        self.assertEqual(kmeans.iterations, 3)
