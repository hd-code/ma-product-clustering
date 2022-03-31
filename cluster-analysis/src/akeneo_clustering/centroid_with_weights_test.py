import unittest

from .centroid_with_weights import create_centroid_cls_with_weights


class Test_CentroidWithWeights(unittest.TestCase):
    def test_calc_distance(self):
        weights = {"a1": 3.0}
        cls = create_centroid_cls_with_weights(weights)

        test_cases = [
            (
                "numerical simple",
                {"a1": 0.5, "a2": 0.2, "a3": 0.6},
                {"a1": 0.2, "a2": 0.2, "a3": 0.8},
                1.1 / 5,
            ),
            (
                "numerical weighted is missing",
                {"a2": 0.2, "a3": 0.6},
                {"a2": 0.2, "a3": 0.8},
                0.2 / 2,
            ),
            (
                "categorical simple",
                {"a1": "a", "a2": "a", "a3": "a"},
                {"a1": "b", "a2": "a", "a3": "b"},
                4 / 5,
            ),
        ]
        for name, p1, p2, want in test_cases:
            with self.subTest(name):
                centroid = cls.init()
                centroid.on_add_point(p1)
                got = centroid.calc_distance(p2)
                self.assertAlmostEqual(got, want)
