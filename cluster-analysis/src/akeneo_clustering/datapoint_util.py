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
