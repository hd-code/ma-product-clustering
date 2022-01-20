from __future__ import annotations

from abc import ABC, abstractmethod


class Datapoint(ABC):
    """Interface for a single Datapoint used in clustering
    
    The dataset to be clustered must be a list of objects, that all implement
    this interface. It specifies who the distance between two points is 
    calculated.
    """

    @abstractmethod
    def calc_distance(self, datapoint: Datapoint) -> float:
        """Calculates the distance between two datapoints
        
        The higher the distance the further apart the two points are from each
        other.
        """
        raise NotImplementedError
