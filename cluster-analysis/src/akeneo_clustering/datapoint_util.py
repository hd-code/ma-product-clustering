import numpy as np

from .datapoint import Datapoint
from .distance import distance


def calc_proximity_matrix(dataset: list[Datapoint]) -> np.ndarray:
    n = len(dataset)
    result = np.zeros((n, n))

    for i in range(n):
        for j in range(i + 1, n):
            result[i][j] = distance(dataset[i], dataset[j])

    return result + result.T  # copy upper triangle to lower triangle


def transform_multi_to_single_cat(dataset: list[Datapoint]) -> list[Datapoint]:
    result = []
    for datapoint in dataset:
        entry = {**datapoint}
        for key, value in entry.items():
            if type(value) == set:
                value_ord = list(value)
                value_ord.sort()
                entry[key] = ",".join(value_ord)
        result.append(Datapoint(entry))
    return result


def overweight_attributes(
    dataset: list[Datapoint], attribute_codes: list[str], factor: int = 2
) -> list[Datapoint]:
    result = []
    for datapoint in dataset:
        entry = {**datapoint}
        for key, value in entry.copy().items():
            if key in attribute_codes:
                for i in range(1, factor):
                    next_key = f"{key}_{i}"
                    entry[next_key] = value
        result.append(Datapoint(entry))
    return result
