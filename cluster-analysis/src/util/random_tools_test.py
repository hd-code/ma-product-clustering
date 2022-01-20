import unittest

from .random_tools import random_int_set


class Test_RandomTools(unittest.TestCase):

    def test_random_int_set(self):
        test_cases = [
            ("normal", 5, 1, 10, None),
            ("full range", 5, 1, 5, None),
            ("too many", 6, 1, 5, AssertionError),
            ("wrong order, still works", 5, 5, 1, None),
            ("with negative", 10, -10, 10, None),
            ("only negative, wrong order", 10, -10, -20, None),
        ]
        for name, num_of_entries, start, end, want_error in test_cases:
            with self.subTest(name):
                if want_error:
                    with self.assertRaises(want_error):
                        random_int_set(num_of_entries, start, end)
                else:
                    got = random_int_set(num_of_entries, start, end)
                    self.assertEqual(len(got), num_of_entries)
                    for value in got:
                        self.assertGreaterEqual(value, min(start, end))
                        self.assertLessEqual(value, max(start, end))
