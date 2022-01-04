from typing import Union
import unittest

from akeneo.util import clean_response


class Test_AkeneoUtil(unittest.TestCase):
    def test_clean_response(self):
        test_cases: list[tuple[str, Union[dict, list], Union[dict, list]]] = [
            (
                "dict with empty values",
                {
                    "bool": True,
                    "string": "Hello World",
                    "empty list": [],
                    "empty dict": {},
                },
                {
                    "bool": True,
                    "string": "Hello World",
                }
            ),
            (
                "dict with underscore keys",
                {
                    "bool": True,
                    "string": "Hello World",
                    "_hiddenKey": "Hello World",
                },
                {
                    "bool": True,
                    "string": "Hello World",
                }
            ),
            (
                "dict with nested empty values",
                {
                    "bool": True,
                    "string": "Hello World",
                    "list": [1, 2, 3],
                    "nested empty list": [[], {}],
                    "list with nested empty": [1, 2, [], 3, 4, {}, 5],
                    "nested empty dict": {
                        "dict": {},
                        "list": [],
                    },
                }, {
                    "bool": True,
                    "string": "Hello World",
                    "list": [1, 2, 3],
                    "list with nested empty": [1, 2, 3, 4, 5],
                }
            ),
            ("empty dict", {}, {}),
            ("empty list", [], []),
            (
                "list with empty values",
                [1, 2, 3, None, 4, 5, None, 6, 7],
                [1, 2, 3, 4, 5, 6, 7]
            ),
            (
                "list with nested empty values",
                [1, 2, [[], []], 3, 4, None, 5, 6, {1: None, 2: []}, 7],
                [1, 2, 3, 4, 5, 6, 7],
            ),
            (
                "non-empty dict",
                {
                    "bool": True,
                    "string": "Hello World",
                    "empty string": "",
                    "number": 3.12,
                    "dict": {
                        "key": "value",
                    },
                    "list of numbers": [1, 2, 3],
                    "list of strings": ["one", "two", "three"],
                },
                {
                    "bool": True,
                    "string": "Hello World",
                    "empty string": "",
                    "number": 3.12,
                    "dict": {
                        "key": "value",
                    },
                    "list of numbers": [1, 2, 3],
                    "list of strings": ["one", "two", "three"],
                },
            ),
            (
                "non-empty list",
                ["one", "two", "three"],
                ["one", "two", "three"],
            )
        ]

        for (name, input, want) in test_cases:
            with self.subTest(name):
                got = clean_response(input)
                self.assertEqual(got, want)
