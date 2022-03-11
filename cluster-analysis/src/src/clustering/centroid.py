from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, Type, TypeVar

Datapoint = TypeVar("Datapoint")


class Centroid(ABC, Generic[Datapoint]):
    """Interface for the centroid of a partition clustering

    It should represent the cluster it belongs to and be being a kind of summary
    of all datapoints within the cluster. Typically, this is the mean for
    numerical attributes and the mode for categorical.
    """

    @classmethod
    @abstractmethod
    def init(cls: Type[Centroid]) -> Centroid:
        """Creates a centroid for a clustering"""
        raise NotImplementedError

    @abstractmethod
    def calc_distance(self, datapoint: Datapoint) -> float:
        """Calculates the distance between the centroid and a single datapoint

        The higher the distance the further apart the datapoint is from the
        centroid.
        """
        raise NotImplementedError

    @abstractmethod
    def on_add_point(self, datapoint: Datapoint) -> None:
        """Called when a datapoint is added to the cluster of this centroid

        Should update the centroid. Might be called in quick succession.
        """
        raise NotImplementedError
