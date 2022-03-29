import random
import unittest

from .inits import random_init


class Test_inits(unittest.TestCase):
    def test_random_init(self):
        random.seed(0)

        n = 100
        k = 10

        points = [0] * n

        with self.subTest("should always have k entries"):
            for _ in range(999):
                got = random_init(points, k)
                self.assertEqual(len(got), k)
