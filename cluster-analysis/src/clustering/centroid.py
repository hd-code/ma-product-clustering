from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Type

from .datapoint import Datapoint


class Centroid(ABC):
    """Interface for the centroid of a partition clustering

    It should represent the cluster it belongs to and be being a kind of summary
    of all datapoints within the cluster. Typically, this is the mean for
    numerical attributes and the mode for categorical.
    """

    @classmethod
    @abstractmethod
    def init_from_datapoint(cls: Type[Centroid], datapoint: Datapoint) -> Centroid:
        """Creates a centroid from a chosen datapoint

        `KMeans` chooses some datapoints at random as initial centroids of the
        clusters. This method specifies, how a centroid is created from a chosen
        datapoint. The chosen Datapoint is also the first member in this cluster.
        """
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

        The centroid might be updated with each new member in the cluster or
        after a complete run through the dataset. See `on_restart`
        """
        raise NotImplementedError

    @abstractmethod
    def on_restart(self) -> None:
        """Called when another iteration of the `KMeans` is started

        This can be used to update the centroid before the next run, reset
        some counter or anything else.
        """
        raise NotImplementedError