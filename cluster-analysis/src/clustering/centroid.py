from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Type

from .datapoint import Datapoint


class Centroid(ABC):
    """Interface for the Centroid of a partition clustering

    It should represent the cluster it belongs to and be being a kind of summary
    of all datapoints within the cluster. Typically, this is the mean for
    numerical attributes and the mode for categorical.
    """

    @classmethod
    @abstractmethod
    def create(cls: Type[Centroid], dataset: list[Datapoint], num_of_points: int) -> list[Centroid]:
        """Creates a list of Centroids
        
        Typically the initial centroid are chosen from random points in the
        dataset. More advanced methods may be used as well.
        """
        raise NotImplementedError

    @abstractmethod
    def calc_distance(self, datapoint: Datapoint) -> float:
        """Calculates the distance between the centroid and a single Datapoint
        
        The higher the distance the further apart the Datapoint is from the
        Centroid.
        """
        raise NotImplementedError

    @abstractmethod
    def on_add_point(self, datapoint: Datapoint) -> None:
        """Called when a Datapoint is added to the cluster of this Centroid
        
        The Centroid might be updated with each new member in the cluster or
        after a complete run through the dataset. See `on_restart`
        """
        raise NotImplementedError

    @abstractmethod
    def on_restart(self) -> None:
        """Called when another iteration of the KMeans is started
        
        This can be used to update the Centroid before the next run, reset some
        counter or anything else.
        """
        raise NotImplementedError
