import math
import unittest

from .centroid2d import Centroid2D, Datapoint2D


class Test_Centroid2D(unittest.TestCase):
    def test_init(self):
        want = Centroid2D(0, 0, 0)
        got = Centroid2D.init()
        self.assertEqual(got, want)

    def test_calc_distance(self):
        point1 = Datapoint2D(1, 2)
        point2 = Datapoint2D(5, 3)
        point3 = Datapoint2D(3, 3)
        point4 = Datapoint2D(-4, 4)

        test_cases: list[tuple[str, Datapoint2D, Datapoint2D, float]] = [
            ("d(p1,p2)", point1, point2, math.sqrt(16 + 1)),
            ("d(p2,p3)", point2, point3, math.sqrt(4 + 0)),
            ("d(p3,p4)", point3, point4, math.sqrt(49 + 1)),
            ("d(p1,p3)", point1, point3, math.sqrt(4 + 1)),
            ("d(p3,p1)", point3, point1, math.sqrt(4 + 1)),
            ("d(p1,p4)", point1, point4, math.sqrt(25 + 4)),
            ("d(p4,p1)", point4, point1, math.sqrt(25 + 4)),
            ("d(p1,p1)", point1, point1, 0.0),
            ("d(p2,p2)", point2, point2, 0.0),
            ("d(p3,p3)", point3, point3, 0.0),
            ("d(p4,p4)", point4, point4, 0.0),
        ]
        for name, p1, p2, want in test_cases:
            with self.subTest(name):
                mp = Centroid2D(p1.x, p1.y, 1)
                got = mp.calc_distance(p2)
                self.assertEqual(got, want)

    def test_on_add_point(self):
        MP = Centroid2D
        DP = Datapoint2D

        test_cases = [
            (MP(1, 2, 1), DP(1, 2), MP(1, 2, 2)),
            (MP(1, 2, 1), DP(2, 1), MP(1.5, 1.5, 2)),
            (MP(4, 2, 4), DP(14, -3), MP(6, 1, 5)),
        ]
        for centroid, datapoint, want in test_cases:
            with self.subTest(f"{centroid} + {datapoint}"):
                centroid.on_add_point(datapoint)
                self.assertEqual(centroid, want)
