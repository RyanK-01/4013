"""
Recommendation Engine  (<<control>>)

Filters and ranks approved stalls based on user-selected preferences:
budget, dietary restrictions, cuisine type, proximity, and popularity.
Scores each stall (popularity pts + proximity pts + favourite boost) 
/ maybe different formula from use case description
and returns results sorted by descending score.
"""

from sqlalchemy.orm import Session

from app.models.stall import Stall, StallDietaryTag
from app.models.favourite import Favourite
from app.schemas.recommendation import FilterSelection
from app.services.location import haversine_distance


def get_recommendations(
    db: Session,
    filters: FilterSelection,
    user_id: int | None = None,
) -> list[dict]:
    def get_recommendations(
    db: Session,
    filters: FilterSelection,
    user_id: int | None = None,
) -> list[dict]:
    """
    Generate ranked stall recommendations based on user preferences.

    This function gets approved stalls from the database, applies
    filtering criteria (e.g. budget, dietary restrictions, cuisine, and proximity),
    and calculates a score for each stall based on different factors such as popularity,
    distance, and user preferences.

    Args:
        db: Database session for querying stall data.
        filters: User-selected filters for narrowing recommendations.
        user_id: Optional user ID for incorporating personalization
                 (e.g. favourites).

    Returns:
        A list of dictionaries containing stall information, distance,
        and computed score, sorted in descending order of relevance.

    Notes:
        Used by the recommendation API endpoint to provide personalised
        stall suggestions to the frontend.
    """
    # TODO: query approved stalls, apply budget/dietary/cuisine/proximity filters,
    #       score each result (popularity + proximity + fav boost) or use diff formula from use case desc, sort descending
    pass
