import unittest

import numpy as np
import numpy.testing as npt

from .datapoint import Datapoint
from .datapoint_util import (
    calc_proximity_matrix,
    overweight_attributes,
    transform_multi_to_single_cat,
)


class Test_DatapointUtil(unittest.TestCase):
    def test_calc_proximity_matrix(self):
        test_cases = [
            (
                "numerical",
                [
                    Datapoint({"a1": 0.5, "a2": 0.2, "a3": 0.6}),
                    Datapoint({"a1": 0.2, "a2": 0.2, "a3": 0.8}),
                    Datapoint({"a1": 0.0, "a2": 0.1, "a3": 0.5}),
                ],
                [
                    [0.0, 0.5 / 3, 0.7 / 3],
                    [0.5 / 3, 0.0, 0.6 / 3],
                    [0.7 / 3, 0.6 / 3, 0.0],
                ],
            ),
            (
                "categorical",
                [
                    Datapoint({"a1": "a", "a2": "a", "a3": "a"}),
                    Datapoint({"a1": "b", "a2": "b", "a3": "b"}),
                    Datapoint({"a1": "a", "a2": "b", "a3": "c"}),
                    Datapoint({"a1": "c", "a2": "b", "a3": "b"}),
                ],
                [
                    [0.0, 3 / 3, 2 / 3, 3 / 3],
                    [3 / 3, 0.0, 2 / 3, 1 / 3],
                    [2 / 3, 2 / 3, 0.0, 2 / 3],
                    [3 / 3, 1 / 3, 2 / 3, 0.0],
                ],
            ),
        ]
        for name, dataset, want in test_cases:
            with self.subTest(name):
                got = calc_proximity_matrix(dataset)
                npt.assert_almost_equal(got, np.array(want))

    def test_transform_multi_to_single_cat(self):
        test_cases = [
            (
                "no transform",
                [Datapoint({"a": 0.5, "b": "name"})],
                [Datapoint({"a": 0.5, "b": "name"})],
            ),
            (
                "one transform",
                [Datapoint({"a": 0.5, "b": "name", "c": {"1", "2", "3"}})],
                [Datapoint({"a": 0.5, "b": "name", "c": "1,2,3"})],
            ),
            (
                "all transforms",
                [Datapoint({"a": {"a"}, "b": {"a", "b"}, "c": {"1", "2", "3"}})],
                [Datapoint({"a": "a", "b": "a,b", "c": "1,2,3"})],
            ),
        ]
        for name, arg, want in test_cases:
            with self.subTest(name):
                got = transform_multi_to_single_cat(arg)
                self.assertListEqual(got, want)

    def test_overweight_attributes(self):
        test_cases = [
            (
                "no overweight",
                [Datapoint({"a": 0.5, "b": "name"})],
                ["c", "d"],
                2,
                [Datapoint({"a": 0.5, "b": "name"})],
            ),
            (
                "overweight some once",
                [Datapoint({"a": 0.5, "b": "name", "c": {"1", "2", "3"}})],
                ["c", "d"],
                2,
                [
                    Datapoint(
                        {
                            "a": 0.5,
                            "b": "name",
                            "c": {"1", "2", "3"},
                            "c_1": {"1", "2", "3"},
                        }
                    )
                ],
            ),
            (
                "overweight some twice",
                [Datapoint({"a": 0.5, "b": "name", "c": {"1", "2", "3"}})],
                ["c", "d"],
                3,
                [
                    Datapoint(
                        {
                            "a": 0.5,
                            "b": "name",
                            "c": {"1", "2", "3"},
                            "c_1": {"1", "2", "3"},
                            "c_2": {"1", "2", "3"},
                        }
                    )
                ],
            ),
            (
                "overweight all once",
                [Datapoint({"a": 0.5, "b": "name", "c": {"1", "2", "3"}})],
                ["a", "b", "c", "d"],
                2,
                [
                    Datapoint(
                        {
                            "a": 0.5,
                            "a_1": 0.5,
                            "b": "name",
                            "b_1": "name",
                            "c": {"1", "2", "3"},
                            "c_1": {"1", "2", "3"},
                        }
                    )
                ],
            ),
        ]
        for name, dataset, attr, factor, want in test_cases:
            with self.subTest(name):
                got = overweight_attributes(dataset, attr, factor)
                self.assertListEqual(got, want)
