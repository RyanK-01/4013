"""
Recommendation Schemas  (<<datatype>>)

Filter payload sent by the client to the recommendation engine.
Covers five dimensions: budget, dietary, proximity, popularity, favourites.
"""

from pydantic import BaseModel


class FilterSelection(BaseModel):
    """User-selected filters for stall recommendations."""
    # TODO: define budget fields (budget_type, budget_exact, budget_min, budget_max)
    # TODO: define dietary fields (dietary_restrictions list, dietary_requirements list, dietary_other)
    # TODO: define proximity fields (proximity_type, latitude, longitude, max_distance_km)
    # TODO: define use_popularity (bool), use_favourites (bool), recommendation_mode (str)
    pass
