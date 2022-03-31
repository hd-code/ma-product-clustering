from __future__ import annotations

from typing import Type

from src import clustering

from .datapoint import Datapoint
from .distance import distance


class Centroid(clustering.Centroid[Datapoint]):
    def __init__(self) -> None:
        self._values = Datapoint({})  # type: ignore
        self._has_changed = False

        self._means: dict[str, tuple[float, int]] = {}
        self._modes: dict[str, dict[str, int]] = {}
        self._modes_multi: dict[str, dict[str, int]] = {}

    @classmethod
    def init(cls: Type[Centroid]) -> Centroid:
        return cls()

    def calc_distance(self, datapoint: Datapoint) -> float:
        if self._has_changed:
            self._update_values()
        return distance(self._values, datapoint)

    def on_add_point(self, datapoint: Datapoint) -> None:
        self._has_changed = True

        add_value = {
            float: lambda key, value: self._add_numerical(key, value),
            str: lambda key, value: self._add_categorical(key, value),
            set: lambda key, value: self._add_multi_categorical(key, value),
        }

        for key, value in datapoint.items():
            add_value[type(value)](key, value)

    # --------------------------------------------------------------------------

    def _add_numerical(self, key: str, value: float) -> None:
        if key not in self._means:
            self._means[key] = value, 1
        else:
            prev_value, n = self._means[key]
            self._means[key] = ((prev_value * n + value) / (n + 1), n + 1)

    def _add_categorical(self, key: str, value: str) -> None:
        if key not in self._modes:
            self._modes[key] = {}
        if value not in self._modes[key]:
            self._modes[key][value] = 1
        else:
            self._modes[key][value] += 1

    def _add_multi_categorical(self, key: str, value: set[str]) -> None:
        if key not in self._modes_multi:
            self._modes_multi[key] = {}
        if value:
            for entry in value:
                if entry not in self._modes_multi[key]:
                    self._modes_multi[key][entry] = 1
                else:
                    self._modes_multi[key][entry] += 1

    # --------------------------------------------------------------------------

    def _update_values(self) -> None:
        self._values.clear()
        self._has_changed = False

        for key, (mean, _) in self._means.items():
            self._values[key] = mean

        for key, words in self._modes.items():
            best_word = ""
            best_word_count = -1
            for word, count in words.items():
                if count > best_word_count:
                    best_word = word
                    best_word_count = count
            self._values[key] = best_word

        for key, words in self._modes_multi.items():
            best_words = set()
            best_words_count = -1
            for word, count in words.items():
                if count == best_words_count:
                    best_words.add(word)
                if count > best_words_count:
                    best_words = {word}
                    best_words_count = count
            self._values[key] = best_words
