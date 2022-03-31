import unittest

from .distance import distance


class Test_distance(unittest.TestCase):
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
                {"a1": {"a", "b"}, "a2": {"a", "b"}, "a3": {"a", "b"}},
                {"a1": {"a", "b"}, "a2": {"a", "c"}, "a3": {"a", "b"}},
                (1 - 1 / 3) / 3,
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
                got = distance(p1, p2)
                self.assertAlmostEqual(want, got)

    def test_calc_distance_with_weights(self):
        test_cases = [
            (
                "numerical",
                {"a1": 0.5, "a2": 0.2, "a3": 0.6},
                {"a1": 0.2, "a2": 0.2, "a3": 0.8},
                {"a1": 1.0, "a2": 2.0, "a3": 1.0},
                0.5 / 4,
            ),
            (
                "numerical with some weights",
                {"a1": 0.5, "a2": 0.2, "a3": 0.6},
                {"a1": 0.2, "a2": 0.6, "a3": 0.8},
                {"a1": 5.0},
                2.1 / 7,
            ),
            (
                "categorical",
                {"a1": "a", "a2": "a", "a3": "a"},
                {"a1": "b", "a2": "a", "a3": "a"},
                {"a1": 1.0, "a2": 3.0, "a3": 1.0},
                1 / 5,
            ),
            (
                "categorical with some weights",
                {"a1": "a", "a2": "a", "a3": "a"},
                {"a1": "b", "a2": "a", "a3": "a"},
                {"a1": 5.0},
                5 / 7,
            ),
            (
                "multi",
                {"a1": {"a", "b"}, "a2": {"a", "b"}, "a3": {"a", "b"}},
                {"a1": {"a", "b"}, "a2": {"a", "c"}, "a3": {"a", "b"}},
                {"a1": 1.0, "a2": 3.0, "a3": 1.0},
                (1 - 1 / 3) * 3 / 5,
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
                {"a1": 3.0, "a5": 0.5},
                4.1 / 8.5,
            ),
        ]
        for name, p1, p2, weights, want in test_cases:
            with self.subTest(name):
                got = distance(p1, p2, weights)
                self.assertAlmostEqual(want, got)
