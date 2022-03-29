import unittest

from .centroid import Centroid


class Test_Centroid(unittest.TestCase):
    def test_init(self):
        got = Centroid.init()
        self.assertIsInstance(got, Centroid)

    def test_calc_distance(self):
        test_cases = [
            (
                "numerical only",
                {"a1": 0.5, "a2": 0.2, "a3": 0.6},
                {"a1": 0.2, "a2": 0.2, "a3": 0.8},
                0.5 / 3,
            ),
            (
                "numerical with missing",
                {"a1": 0.5, "a2": 0.2, "a3": 0.6},
                {"a1": 0.2, "a3": 0.8},
                1.5 / 3,
            ),
            (
                "categorical only",
                {"a1": "a", "a2": "a", "a3": "a"},
                {"a1": "b", "a2": "a", "a3": "a"},
                1 - 2 / 3,
            ),
            (
                "categorical with missing",
                {"a1": "a", "a2": "a", "a3": "a"},
                {"a1": "b", "a3": "a"},
                1 - 1 / 3,
            ),
            (
                "mixed example",
                {"a1": 0.5, "a2": 0.2, "a4": "m", "a5": "xl", "a6": "s", "a8": {"red"}},
                {
                    "a1": 0.3,
                    "a2": 0.2,
                    "a3": 0.6,
                    "a4": "l",
                    "a5": "xl",
                    "a8": {"red", "green"},
                },
                3.7 / 7,
            ),
        ]
        for name, p1, p2, want in test_cases:
            with self.subTest(name):
                c = Centroid()
                c.on_add_point(p1)
                got = c.calc_distance(p2)
                self.assertAlmostEqual(got, want)

    def test_on_add_point(self):
        test_cases = [
            (
                "mixed example",
                [
                    {"a": 0.3, "b": 0.5, "c": "l", "d": {"red"}},
                    {"a": 0.7, "c": "m", "d": {"red"}},
                    {"a": 0.2, "b": 0.5, "c": "m"},
                    {"a": 0.8, "c": "s", "d": {"green"}},
                    {"a": 0.3, "c": "m", "d": {"green", "red"}},
                ],
                {"a": 2.3 / 5, "b": 0.5, "c": "m", "d": {"red"}},
            )
        ]
        for name, points, want in test_cases:
            with self.subTest(name):
                c = Centroid()
                [c.on_add_point(p) for p in points]
                c._update_values()
                self.assertEqual(c._values, want)

    def test_init_with_one_point(self):
        test_cases = [
            (
                "numerical only",
                {"a1": 0.5, "a2": 0.2, "a3": 0.6},
                0.0,
            ),
            (
                "categorical only",
                {"a1": "a", "a2": "a", "a3": "a"},
                0.0,
            ),
            (
                "mixed example",
                {
                    "a1": 0.3,
                    "a2": 0.2,
                    "a3": 0.6,
                    "a4": "l",
                    "a5": "xl",
                    "a8": {"red", "green"},
                },
                0.08333333333333333,
            ),
        ]
        for name, point, want in test_cases:
            with self.subTest(name):
                c = Centroid()
                c.on_add_point(point)
                got = c.calc_distance(point)
                self.assertAlmostEqual(got, want)
