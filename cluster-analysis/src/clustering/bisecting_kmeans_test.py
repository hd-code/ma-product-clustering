import unittest

import numpy.testing as npt

from .bisecting_kmeans import BisectingKMeans
from .centroid2d import Centroid2D, Datapoint2D


class Test_BisectingKMeans(unittest.TestCase):
    def test_dataset(self):
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

        bi_kmeans = BisectingKMeans(data, Centroid2D, random_state=0)

        with self.subTest("check 2 clusters"):
            self.assertListEqual(
                bi_kmeans.labels_flat(2), [0, 0, 0, 0, 0, 1, 1, 1, 1, 1]
            )

        with self.subTest("check 4 clusters"):
            self.assertListEqual(
                bi_kmeans.labels_flat(4), [0, 0, 0, 2, 3, 1, 1, 1, 1, 1]
            )

        with self.subTest("check if all points in their own cluster"):
            all_in_own = bi_kmeans.labels_flat(len(data))
            all_in_own_set = set(all_in_own)
            self.assertEqual(len(all_in_own), len(all_in_own_set))

    def test_with_duplicates(self):
        data = [
            Datapoint2D(0, 0),
            Datapoint2D(0, 1),
            Datapoint2D(1, 0),
            Datapoint2D(1, 1),
            Datapoint2D(0, 0),
        ]

        bi_kmeans = BisectingKMeans(data, Centroid2D, random_state=0)

        with self.subTest("check 2 clusters"):
            self.assertListEqual(bi_kmeans.labels_flat(2), [0, 0, 0, 1, 0])

        with self.subTest("check 4 clusters"):
            self.assertListEqual(bi_kmeans.labels_flat(4), [0, 3, 2, 1, 0])

        with self.subTest("check 5 clusters"):
            self.assertListEqual(bi_kmeans.labels_flat(5), [0, 3, 2, 1, 4])

    def test_dendrogram(self):
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

        bi_kmeans = BisectingKMeans(data, Centroid2D, random_state=0)
        got = bi_kmeans.dendrogram_matrix

        self.assertEqual((len(data) - 1, 4), got.shape)
