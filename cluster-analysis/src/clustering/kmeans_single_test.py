import unittest

import numpy as np
import numpy.testing as npt

from .centroid2d import Centroid2D, Datapoint2D
from .inits import linear_init
from .kmeans_single import KMeansSingle


class Test_KMeansSingle(unittest.TestCase):
    def test_same_number_of_points_and_clusters(self):
        test_range = range(1, 7)
        points = [Datapoint2D(i, i) for i in test_range]

        for i in test_range:
            with self.subTest(f"{i} clusters and points"):
                data = points[:i]
                got = KMeansSingle(data, Centroid2D, i, init=linear_init)
                npt.assert_array_equal(got.labels, np.array(range(i)))
                self.assertEqual(got.iterations, 1)
                self.assertEqual(got.error, 0)

    def test_data_set(self):
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

        test_cases = [
            (2, [0, 0, 0, 1, 0, 1, 1, 1, 1, 1], 5, 13.48272903487812),
            (3, [0, 0, 2, 2, 0, 1, 1, 1, 1, 1], 4, 10.447975026066313),
            (4, [1, 1, 2, 2, 0, 0, 3, 3, 3, 3], 3, 7.8899799375550215),
            (7, [0, 1, 2, 3, 4, 5, 6, 6, 6, 6], 2, 3.0615528128088307),
            (10, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], 1, 0),
        ]
        for k, want, want_iter, error_ in test_cases:
            with self.subTest(f"{k} clusters"):
                got = KMeansSingle(points, Centroid2D, k, init=linear_init)
                npt.assert_array_equal(got.labels, np.array(want))
                self.assertEqual(got.iterations, want_iter)
                self.assertAlmostEqual(got.error, error_)

    def test_same_points(self):
        points = [
            Datapoint2D(0, 3),
            Datapoint2D(0, 3),
            Datapoint2D(0, 3),
            Datapoint2D(1, 0),
        ]
        want = [0, 1, 2, 0]

        got = KMeansSingle(points, Centroid2D, 3, init=linear_init)
        npt.assert_array_equal(got.labels, np.array(want))
        self.assertEqual(got.iterations, 1)
        self.assertAlmostEqual(got.error, 3.1622776601683795)

    def test_strange_points(self):
        points = [
            Datapoint2D(0, 0),
            Datapoint2D(0, 0),
            Datapoint2D(2, 2),
            Datapoint2D(2, 2),
        ]
        want = [0, 1, 2, 2]

        got = KMeansSingle(points, Centroid2D, 3, init=linear_init)
        npt.assert_array_equal(got.labels, np.array(want))
        self.assertEqual(got.iterations, 2)
        self.assertAlmostEqual(got.error, 0.0)
