import unittest

from .centroid2d import Centroid2D
from .datapoint2d import Datapoint2D
from .kmeans import KMeans


class Test_KMeans(unittest.TestCase):

    def test_basic_clustering_and_value_access(self):
        points = [
            Datapoint2D(0, 0),
            Datapoint2D(0, 1),
            Datapoint2D(1, 0),
            Datapoint2D(2, 2),
            Datapoint2D(2, 3),
            Datapoint2D(3, 2),
        ]
        kmeans1 = KMeans(points, Centroid2D, 2, num_of_trys=1)
        kmeans2 = KMeans(points, Centroid2D, 2, num_of_trys=2)

        self.assertListEqual(kmeans1.result, [0, 0, 0, 1, 1, 1])
        self.assertEqual(len(kmeans1.mean_distances), 2)
        self.assertAlmostEqual(*kmeans1.mean_distances)

        # should all be the same, because cluster init is deterministic
        self.assertListEqual(kmeans1.result, kmeans2.result)
        self.assertListEqual(kmeans1.mean_distances,
                             kmeans2.mean_distances)
        self.assertEqual(kmeans1.iterations, kmeans2.iterations)
