"""
Location Service  (<<control>>)

Provides the Haversine formula for calculating great-circle distance (in km)
between two GPS coordinate pairs. Used by the recommendation engine and
nearby-stalls endpoint for proximity filtering and sorting.
Light weight function to calculate the distance between 2 points.
"""

import math


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate the great-circle distance (km) between two lat/lon points.

    This function utilises the Haversine formula to compute the shortest
    distance over the Earth's surface between two latitude/longitude points.

    Args:
        lat1: Latitude of the first point (in decimal degrees).
        lon1: Longitude of the first point (in decimal degrees).
        lat2: Latitude of the second point (in decimal degrees).
        lon2: Longitude of the second point (in decimal degrees).

    Returns:
        Distance between the two points in kilometres.

    Notes:
        Used for proximity-based filtering and ranking of nearby stalls.
    
    
    """
    # TODO: implement Haversine formula using Earth radius 6371 km to track 
    pass
