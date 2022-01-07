import unittest

from clustering.cluster import Cluster
from clustering.data_point_3d import DataPoint3DVector
from clustering.middle_point_3d import MiddlePoint3DVector


class Test_Cluster(unittest.TestCase):
    def setUp(self) -> None:
        self.middle_point = MiddlePoint3DVector(1, 2, 3, 0)
        self.cluster = Cluster(self.middle_point)

    def test_add_point(self):
        data_point_1 = DataPoint3DVector(0, 3, 4, 5)
        data_point_2 = DataPoint3DVector(1, 5, 2, 9)

        self.cluster.add_point(data_point_1)
        self.assertEqual(len(self.cluster.members), 1)
        self.assertIs(self.cluster.members[0], data_point_1)
        self.assertEqual(self.cluster.middle_point.x, data_point_1.x)
        self.assertEqual(self.cluster.middle_point.y, data_point_1.y)
        self.assertEqual(self.cluster.middle_point.z, data_point_1.z)
        self.assertIs(data_point_1.get_cluster(), self.cluster)

        self.cluster.add_point(data_point_2)
        self.assertEqual(len(self.cluster.members), 2)
        self.assertIs(self.cluster.members[1], data_point_2)
        self.assertEqual(self.cluster.middle_point.x, 8 / 2)
        self.assertEqual(self.cluster.middle_point.y, 6 / 2)
        self.assertEqual(self.cluster.middle_point.z, 14 / 2)
        self.assertIs(data_point_2.get_cluster(), self.cluster)

    def test_calc_distance(self):
        data_point_1 = DataPoint3DVector(0, 3, 4, 5)
        data_point_2 = DataPoint3DVector(1, 5, 2, 9)

        want = self.middle_point.calc_distance(data_point_1)
        got = self.cluster.calc_distance(data_point_1)
        self.assertEqual(got, want)

        want = self.middle_point.calc_distance(data_point_2)
        got = self.cluster.calc_distance(data_point_2)
        self.assertEqual(got, want)

    def test_restart(self):
        data_point_1 = DataPoint3DVector(0, 3, 4, 5)
        data_point_2 = DataPoint3DVector(1, 5, 2, 9)

        self.cluster.add_point(data_point_1)
        self.cluster.add_point(data_point_2)
        self.assertEqual(len(self.cluster.members), 2)

        self.cluster.restart()

        self.assertEqual(len(self.cluster.members), 0)
        self.assertEqual(self.cluster.middle_point.x, 8 / 2)
        self.assertEqual(self.cluster.middle_point.y, 6 / 2)
        self.assertEqual(self.cluster.middle_point.z, 14 / 2)
