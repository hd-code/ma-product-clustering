import util
import unittest

from .bisecting_kmeans import BisectingKMeans
from .centroid2d import Centroid2DRandom
from .datapoint2d import Datapoint2D


class Test_BisectingKMeans(unittest.TestCase):

    def test_data_set(self):
        data = [
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
        util.seed()

        bi_kmeans = BisectingKMeans(data, Centroid2DRandom,
                                    kmeans_num_of_trys=5)

        with self.subTest("check 2 clusters"):
            self.assertListEqual(
                bi_kmeans.result_flat(2),
                [1, 1, 1, 0, 0, 0, 0, 0, 0, 0]
            )

        with self.subTest("check 4 clusters"):
            self.assertListEqual(
                bi_kmeans.result_flat(4),
                [1, 1, 1, 2, 3, 3, 0, 0, 0, 0]
            )

        with self.subTest("check if all points in their own cluster"):
            all_in_own = bi_kmeans.result_flat(len(data))
            all_in_own_set = set(all_in_own)
            self.assertEqual(len(all_in_own), len(all_in_own_set))
