import random


def seed(value: int = 0) -> None:
    random.seed(value)


def random_int_set(num_of_entries: int, start: int, end: int) -> set[int]:
    if start > end:
        tmp = start
        start = end
        end = tmp

    assert num_of_entries <= end - start + 1, "range is too narrow"

    result: set[int] = set()
    while len(result) < num_of_entries:
        result.add(random.randint(start, end))

    return result
