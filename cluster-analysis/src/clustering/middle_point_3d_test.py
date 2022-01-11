import unittest

from clustering.data_point_3d import DataPoint3D
from clustering.middle_point_3d import MiddlePoint3D


class Test_MiddlePoint(unittest.TestCase):
    def test_create_points(self):
        data = [
            DataPoint3D(3, 0, 7),
            DataPoint3D(1, 1, 5),
            DataPoint3D(5, 5, 1),
            DataPoint3D(5, 8, 3),
        ]

        middle_points = MiddlePoint3D.create_points(data, 2)
        self.assertEqual(2, len(middle_points))
        for mp in middle_points:
            is_in_list = False
            for dp in data:
                distance = mp.calc_distance(dp)
                if distance == 0:
                    is_in_list = True
            self.assertTrue(
                is_in_list, "MiddlePoint did not match any DataPoint")

    def test_on_add_point_1(self):
        mp = MiddlePoint3D(1, 2, 3, 1)
        dp = DataPoint3D(3, 2, 1)
        mp.on_add_point(dp)

        self.assertAlmostEqual(mp.x, 2)
        self.assertAlmostEqual(mp.y, 2)
        self.assertAlmostEqual(mp.z, 2)
        self.assertAlmostEqual(mp.n, 2)

    def test_on_add_point_2(self):
        mp = MiddlePoint3D(2, 2, 2, 2)
        dp = DataPoint3D(4, 0, 3)
        mp.on_add_point(dp)

        self.assertAlmostEqual(mp.x, (1+3+4) / 3)
        self.assertAlmostEqual(mp.y, (2+2+0) / 3)
        self.assertAlmostEqual(mp.z, (3+1+3) / 3)
        self.assertAlmostEqual(mp.n, 3)

    def test_on_restart(self):
        mp = MiddlePoint3D(2, 2, 2, 2)
        dp = DataPoint3D(4, 0, 3)

        mp.on_restart()
        mp.on_add_point(dp)

        self.assertEqual(mp.x, dp.x)
        self.assertEqual(mp.y, dp.y)
        self.assertEqual(mp.z, dp.z)
        self.assertEqual(mp.n, 1)
