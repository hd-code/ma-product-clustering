"""General tools and framework to perform cluster analysis

It offers interfaces for `Datapoint`s and `Centroid`s as well as the clustering
methods for `KMeans` and `BisectingKMeans`.
"""

from .bisecting_kmeans import BisectingKMeans
from .centroid import Centroid, Datapoint
from .inits import linear_init, random_init
from .kmeans import KMeans
