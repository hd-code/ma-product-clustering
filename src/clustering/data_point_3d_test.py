import math
import unittest

from .data_point_3d import DataPoint3D


class Test_DataPoint3D(unittest.TestCase):
    def test_calc_distance(self):
        point1 = DataPoint3D(6, 2, 4)
        point2 = DataPoint3D(1, 1, 1)
        point3 = DataPoint3D(3, 3, 3)

        want = math.sqrt(25 + 1 + 9)
        got = point1.calc_distance(point2)
        self.assertEqual(got, want)

        want = math.sqrt(4 + 4 + 4)
        got = point2.calc_distance(point3)
        self.assertEqual(got, want)

        want = math.sqrt(9 + 1 + 1)
        got = point1.calc_distance(point3)
        self.assertEqual(got, want)

    def test_calc_distance_same_point(self):
        points = [
            DataPoint3D(6, 2, 4),
            DataPoint3D(1, 1, 1),
            DataPoint3D(3, 3, 3),
        ]
        for point in points:
            got = point.calc_distance(point)
            self.assertEqual(got, 0)
