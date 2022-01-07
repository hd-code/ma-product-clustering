import math
import unittest

from clustering.data_point_3d import DataPoint3DVector
from clustering.middle_point_3d import MiddlePoint3DVector


class Test_MiddlePoint(unittest.TestCase):
    def test_create_points(self):
        data = [
            DataPoint3DVector(0, 3, 0, 7),
            DataPoint3DVector(1, 1, 1, 5),
            DataPoint3DVector(2, 5, 5, 1),
            DataPoint3DVector(3, 5, 8, 3),
        ]

        middle_points = MiddlePoint3DVector.create_points(data, 2)
        self.assertEqual(2, len(middle_points))
        for mp in middle_points:
            is_in_list = False
            for dp in data:
                distance = mp.calc_distance(dp)
                if distance == 0:
                    is_in_list = True
            self.assertTrue(
                is_in_list, "MiddlePoint did not match any DataPoint")

    def test_calc_distance(self):
        mp = MiddlePoint3DVector(1, 2, 3)
        dp = DataPoint3DVector(0, 3, 2, 1)

        want = math.sqrt(4 + 0 + 4)
        got = mp.calc_distance(dp)

        self.assertAlmostEqual(want, got)

    def test_on_add_point_1(self):
        mp = MiddlePoint3DVector(1, 2, 3, 1)
        dp = DataPoint3DVector(0, 3, 2, 1)
        mp.on_add_point(dp)

        self.assertAlmostEqual(mp.x, 2)
        self.assertAlmostEqual(mp.y, 2)
        self.assertAlmostEqual(mp.z, 2)
        self.assertAlmostEqual(mp.n, 2)

    def test_on_add_point_2(self):
        mp = MiddlePoint3DVector(2, 2, 2, 2)
        dp = DataPoint3DVector(0, 4, 0, 3)
        mp.on_add_point(dp)

        self.assertAlmostEqual(mp.x, (1+3+4) / 3)
        self.assertAlmostEqual(mp.y, (2+2+0) / 3)
        self.assertAlmostEqual(mp.z, (3+1+3) / 3)
        self.assertAlmostEqual(mp.n, 3)
