import math
import unittest

from .datapoint2d import Datapoint2D


class Test_Datapoint2D(unittest.TestCase):

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
                got = p1.calc_distance(p2)
                self.assertEqual(got, want)
