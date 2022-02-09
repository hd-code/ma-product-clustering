import unittest

from .centroid import Centroid, Datapoint


class Test_Centroid(unittest.TestCase):
    def test_init_from_datapoint(self):
        point: Datapoint = {
            "color": "red",
            "tags": ["summer", "home"],
            "length": 0.25,
            "height": 1.2,
            "width": 0.4,
        }
        want_means = {
            "length": (0.25, 1),
            "height": (1.2, 1),
            "width": (0.4, 1),
        }
        want_modes = {
            "color": {"red": 1},
            "tags": {"home": 1, "summer": 1},
        }

        got = Centroid.init_from_datapoint(point)

        self.assertEqual(got._values, point)
        self.assertEqual(got._means, want_means)
        self.assertEqual(got._modes, want_modes)

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
                "multi only",
                {"a1": ["a", "b"], "a2": ["a", "b"], "a3": ["a", "b"]},
                {"a1": ["a", "b"], "a2": ["a", "c"], "a3": ["a", "b"]},
                (1 - 1 / 3) / 3,
            ),
            (
                "mixed example",
                {"a1": 0.5, "a2": 0.2, "a4": "m", "a5": "xl", "a6": "s", "a8": "red"},
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
                c = Centroid(p1)
                got = c.calc_distance(p2)
                self.assertAlmostEqual(got, want)

    def test_on_restart(self):
        test_cases = [
            (
                "mixed example",
                {"a": 0.3, "b": 0.5, "c": "l", "d": "red"},
                [
                    {"a": 0.7, "c": {"s", "m"}, "d": "red"},
                    {"a": 0.2, "b": 0.5, "c": "m"},
                    {"a": 0.8, "c": {"s", "l"}, "d": "green"},
                    {"a": 0.3, "c": "m", "d": {"green", "red"}},
                ],
                {"a": 2.3 / 5, "b": 0.5, "c": "m", "d": "red"},
            )
        ]
        for name, init_p, points, want in test_cases:
            with self.subTest(name):
                c = Centroid(init_p)
                [c.on_add_point(p) for p in points]

                c.on_restart()

                self.assertEqual(c._values, want)
                self.assertEqual(c._means, {})
                self.assertEqual(c._modes, {})
