"""Pydantic schema for the recommendation filter payload sent by the client."""

from pydantic import BaseModel


class FilterSelection(BaseModel):
    """User-selected filters for the stall recommendation engine (budget, dietary, proximity, etc.)."""
    # Budget
    budget_type: str | None = None  # "exact" or "range"
    budget_exact: float | None = None
    budget_min: float | None = None
    budget_max: float | None = None

    # Dietary
    dietary_restrictions: list[str] = []  # "Halal", "No seafood", "No nuts", "Vegetarian", "No beef"
    dietary_requirements: list[str] = []  # "Chinese Cuisine", "Malay Cuisine", etc.
    dietary_other: str | None = None  # Custom cuisine text

    # Proximity
    proximity_type: str | None = None  # "current" or "selected"
    latitude: float | None = None
    longitude: float | None = None
    max_distance_km: float | None = None

    # Popularity
    use_popularity: bool = False

    # Favourites
    use_favourites: bool = False

    # Recommendation mode
    recommendation_mode: str = "combined"  # "combined" or "individual"
