from typing import Callable, Type, TypeVar

from .datapoint import Datapoint


def distance(
    p1: Datapoint, p2: Datapoint, sample_weight: dict[str, float] = None
) -> float:
    attr_codes = set(p1.keys()).union(p2.keys())
    n_codes = len(attr_codes)

    if n_codes == 0:
        return 0.0

    distance = 0.0
    n_values = 0.0

    for attr_code in attr_codes:
        weight = (
            1
            if sample_weight is None or attr_code not in sample_weight
            else sample_weight[attr_code]
        )

        if attr_code in p1 and attr_code in p2:
            v1 = p1[attr_code]
            v2 = p2[attr_code]

            distance += weight * _map_type_to_handler[type(v1)](v1, v2)  # type: ignore
            n_values += weight
        else:
            distance += weight  # if one value is missing, add 1 => inverted Jaccard
            n_values += weight

    return distance / n_values  # Jaccard


T = TypeVar("T", float, str, set[str])

_map_type_to_handler: dict[Type[T], Callable[[T, T], float]] = {  # type: ignore
    float: lambda x, y: abs(x - y),  # type: ignore
    str: lambda x, y: 0 if x == y else 1,
    set: lambda x, y: 1 - (len(x.intersection(y)) / len(x.union(y))),  # type: ignore
}
