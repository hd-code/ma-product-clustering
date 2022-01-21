import random
import unittest

from .centroid2d import Centroid2D
from .datapoint2d import Datapoint2D
from .inits import linear_init
from .kmeans import KMeans


class Test_KMeans(unittest.TestCase):

    def test_static_init_static_result(self):
        points = [
            Datapoint2D(0, 0),
            Datapoint2D(0, 1),
            Datapoint2D(1, 0),
            Datapoint2D(2, 2),
            Datapoint2D(2, 3),
            Datapoint2D(3, 2),
        ]
        kmeans1 = KMeans(points, Centroid2D, 2, linear_init, 1)
        kmeans2 = KMeans(points, Centroid2D, 2, linear_init, 2)

        self.assertListEqual(kmeans1.result, [0, 0, 0, 1, 1, 1])
        self.assertAlmostEqual(kmeans1.error, 2.66666666)

        # should all be the same, because cluster init is deterministic
        self.assertListEqual(kmeans1.result, kmeans2.result)
        self.assertEqual(kmeans1.iterations, kmeans2.iterations)
        self.assertEqual(kmeans1.error, kmeans2.error)

    def test_random_init_better_result_with_more_iterations(self):
        points = [
            Datapoint2D(0, 3),
            Datapoint2D(1, 2),
            Datapoint2D(2, 1),
            Datapoint2D(4, 1),
            Datapoint2D(2, 4),
            Datapoint2D(3, 5),
            Datapoint2D(4, 4),
            Datapoint2D(5, 3),
            Datapoint2D(5, 4),
            Datapoint2D(5, 5),
        ]

        random.seed(0)
        kmeans1 = KMeans(points, Centroid2D, 2, n_init=1)

        random.seed(0)
        kmeans2 = KMeans(points, Centroid2D, 2, n_init=5)

        self.assertNotEqual(kmeans1.result, kmeans2.result)
        self.assertGreater(kmeans1.error, kmeans2.error)
