from typing import Callable, Type, TypeVar

from .datapoint import Datapoint


def distance(p1: Datapoint, p2: Datapoint) -> float:
    attr_codes = set(p1.keys()).union(p2.keys())
    if len(attr_codes) == 0:
        return 0.0

    distance = 0.0

    for attr_code in attr_codes:
        if attr_code in p1 and attr_code in p2:
            v1 = p1[attr_code]
            v2 = p2[attr_code]

            distance += _map_type_to_handler[type(v1)](v1, v2)  # type: ignore
        else:
            distance += 1  # if one value is missing, add 1

    return distance / len(attr_codes)


T = TypeVar("T", float, str, set[str])

_map_type_to_handler: dict[Type[T], Callable[[T, T], float]] = {  # type: ignore
    float: lambda x, y: abs(x - y),  # type: ignore
    str: lambda x, y: 0 if x == y else 1,
    set: lambda x, y: 1 - (len(x.intersection(y)) / len(x.union(y))),  # type: ignore
}
