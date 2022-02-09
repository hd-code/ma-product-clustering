from __future__ import annotations

from typing import NewType, Type, Union

import clustering as cl

DataValue = Union[float, str, set[str]]
Datapoint = NewType("Datapoint", dict[str, DataValue])


def _distance(p1: Datapoint, p2: Datapoint) -> float:
    attr_codes = set(p1.keys()).union(p2.keys())
    distance = float(len(attr_codes))

    for attr_code in attr_codes:
        if attr_code in p1 and attr_code in p2:
            if isinstance(p2[attr_code], float):
                distance -= 1.0
                distance += abs(p1[attr_code] - p2[attr_code])
            elif isinstance(p2[attr_code], str):
                if p1[attr_code] == p2[attr_code]:
                    distance -= 1.0
            else:
                p1s = set(
                    p1[attr_code]
                    if isinstance(p1[attr_code], list)
                    else [p1[attr_code]]
                )
                p2s = set(p2[attr_code])

                distance -= len(p1s.intersection(p2s)) / len(p1s.union(p2s))

    return distance / len(attr_codes)


class Centroid(cl.Centroid[Datapoint]):
    def __init__(self, datapoint: Datapoint) -> None:
        self._values = datapoint.copy()

        self._means: dict[str, tuple[float, int]] = {}
        self._modes: dict[str, dict[str, int]] = {}

        self.on_add_point(datapoint)

    @classmethod
    def init_from_datapoint(cls: Type[Centroid], datapoint: Datapoint) -> Centroid:
        return cls(datapoint)

    def calc_distance(self, datapoint: Datapoint) -> float:
        return _distance(self._values, datapoint)

    def on_add_point(self, datapoint: Datapoint) -> None:
        for key, value in datapoint.items():
            if isinstance(value, float):
                if key not in self._means:
                    self._means[key] = value, 1
                else:
                    prev_value, n = self._means[key]
                    self._means[key] = ((prev_value * n + value) / (n + 1), n + 1)
            elif isinstance(value, str):
                if key not in self._modes:
                    self._modes[key] = {}
                if value not in self._modes[key]:
                    self._modes[key][value] = 1
                else:
                    self._modes[key][value] += 1
            else:
                if key not in self._modes:
                    self._modes[key] = {}
                for entry in value:
                    if entry not in self._modes[key]:
                        self._modes[key][entry] = 1
                    else:
                        self._modes[key][entry] += 1

    def on_restart(self) -> None:
        self._values = {}

        for key, value in self._means.items():
            self._values[key] = value[0]

        for key, value in self._modes.items():
            best_word = ""
            best_word_count = -1
            for word, count in value.items():
                if count > best_word_count:
                    best_word = word
                    best_word_count = count

            self._values[key] = best_word

        self._means = {}
        self._modes = {}
