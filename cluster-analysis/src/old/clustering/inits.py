from random import randint
from typing import Callable

from .centroid import Datapoint

InitFunc = Callable[[list[Datapoint], int], set[int]]


def random_init(dataset: list[Datapoint], k: int) -> set[int]:
    result: set[int] = set()
    n = len(dataset)
    while len(result) < k:
        value = randint(0, n - 1)
        result.add(value)
    return result


def linear_init(_: list[Datapoint], k: int) -> set[int]:
    return set(range(k))
