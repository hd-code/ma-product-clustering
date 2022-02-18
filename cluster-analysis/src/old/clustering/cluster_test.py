import unittest
import unittest.mock as mock
from dataclasses import dataclass

from .centroid2d import Datapoint2D
from .cluster import Cluster
from .kmeans import KMeans


class Test_Cluster(unittest.TestCase):
    def test_error_orig(self):
        cluster = Cluster([], [], 0.5)

        cluster.error = 0.2
        self.assertEqual(cluster.error, 0.2)
        self.assertEqual(cluster.error_orig, 0.5)

        cluster.error = 0.8
        self.assertEqual(cluster.error, 0.8)
        self.assertEqual(cluster.error_orig, 0.5)

    def test_splinter_off_better_cluster(self):
        data = [
            Datapoint2D(0, 0),
            Datapoint2D(2, 2),
            Datapoint2D(1, 0),
            Datapoint2D(2, 3),
            Datapoint2D(0, 1),
            Datapoint2D(3, 3),
        ]
        data_i = list(range(len(data)))

        @dataclass
        class TestCase:
            name: str
            init_error: float
            kmeans_result: list[int]
            kmeans_errors: list[float]
            dp_i_remaining: list[int]
            dp_i_splittered: list[int]

        test_cases: list[TestCase] = [
            TestCase(
                "splitter every first other",
                0.8,
                [0, 1, 0, 1, 0, 1],
                [0.5, 0.6],
                [1, 3, 5],
                [0, 2, 4],
            ),
            TestCase(
                "splitter every second other",
                0.8,
                [0, 1, 0, 1, 0, 1],
                [0.6, 0.5],
                [0, 2, 4],
                [1, 3, 5],
            ),
            TestCase(
                "splitter only last",
                0.8,
                [0, 0, 0, 0, 0, 1],
                [0.6, 0.0],
                [0, 1, 2, 3, 4],
                [5],
            ),
        ]
        for tc in test_cases:
            with self.subTest(tc.name):

                def do_kmeans(_):
                    kmeans_mock = mock.Mock(KMeans)
                    kmeans_mock.result = tc.kmeans_result
                    kmeans_mock.error_per_cluster = tc.kmeans_errors
                    return kmeans_mock

                cluster_orig = Cluster(data, data_i, tc.init_error)
                cluster_splt = cluster_orig.splinter_off_better_cluster(do_kmeans)

                self.assertListEqual(cluster_orig.dataset_i, tc.dp_i_remaining)
                self.assertEqual(cluster_orig.error_orig, tc.init_error)
                self.assertEqual(cluster_orig.error, max(tc.kmeans_errors))

                self.assertListEqual(cluster_splt.dataset_i, tc.dp_i_splittered)
                self.assertEqual(cluster_splt.error, min(tc.kmeans_errors))
                self.assertEqual(cluster_splt.error_orig, cluster_splt.error)
