"""Recommendation engine that filters and ranks stalls based on user preferences.

Applies budget, dietary, proximity, and popularity filters, then scores and
ranks results with optional favourites boosting for authenticated users.
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
    """
    Generate food stall recommendations based on user-selected filters.
    Returns a list of stall dicts with optional distance field.
    """
    query = db.query(Stall).filter(Stall.is_approved == True)

    # ── Budget filter ──
    if filters.budget_type == "exact" and filters.budget_exact is not None:
        query = query.filter(Stall.price_range_min <= filters.budget_exact)
    elif filters.budget_type == "range":
        if filters.budget_min is not None:
            query = query.filter(Stall.price_range_max >= filters.budget_min)
        if filters.budget_max is not None:
            query = query.filter(Stall.price_range_min <= filters.budget_max)

    # ── Dietary restrictions filter ──
    # Exclude stalls that have any of the restricted items
    restriction_tag_map = {
        "No seafood": "Seafood",
        "No nuts": "Nuts",
        "No beef": "Beef",
    }
    if filters.dietary_restrictions:
        for restriction in filters.dietary_restrictions:
            if restriction == "Halal":
                # Must have Halal tag
                query = query.filter(
                    Stall.id.in_(
                        db.query(StallDietaryTag.stall_id).filter(StallDietaryTag.tag == "Halal")
                    )
                )
            elif restriction == "Vegetarian":
                query = query.filter(
                    Stall.id.in_(
                        db.query(StallDietaryTag.stall_id).filter(StallDietaryTag.tag == "Vegetarian")
                    )
                )
            elif restriction in restriction_tag_map:
                # Exclude stalls that serve the allergen
                exclude_tag = restriction_tag_map[restriction]
                query = query.filter(
                    ~Stall.id.in_(
                        db.query(StallDietaryTag.stall_id).filter(StallDietaryTag.tag == exclude_tag)
                    )
                )

    # ── Dietary requirements (cuisine) filter ──
    if filters.dietary_requirements:
        cuisine_list = list(filters.dietary_requirements)
        if filters.dietary_other:
            cuisine_list.append(filters.dietary_other)
        query = query.filter(Stall.cuisine_type.in_(cuisine_list))

    # ── Popularity filter (order by Google rating) ──
    # Applied in sorting stage below

    stalls = query.all()

    # ── Proximity filter ──
    results = []
    for stall in stalls:
        stall_dict = {
            "stall": stall,
            "distance": None,
            "score": 0,
        }

        if filters.proximity_type and filters.latitude and filters.longitude and stall.latitude and stall.longitude:
            dist = haversine_distance(
                filters.latitude, filters.longitude,
                stall.latitude, stall.longitude,
            )
            stall_dict["distance"] = round(dist, 2)

            if filters.max_distance_km and dist > filters.max_distance_km:
                continue  # Skip stalls outside range

        results.append(stall_dict)

    # ── Favourites boost ──
    favourite_stall_ids = set()
    if filters.use_favourites and user_id:
        favs = db.query(Favourite.stall_id).filter(Favourite.user_id == user_id).all()
        favourite_stall_ids = {f.stall_id for f in favs}

    # ── Scoring & ranking ──
    for r in results:
        stall = r["stall"]
        score = 0

        # Popularity score
        if filters.use_popularity and stall.google_rating:
            score += stall.google_rating * 10  # 0-50 points

        # Favourite boost
        if stall.id in favourite_stall_ids:
            score += 25

        # Proximity score (closer = higher)
        if r["distance"] is not None:
            score += max(0, 50 - r["distance"])  # Up to 50 points for being close

        r["score"] = score

    # Sort by score descending
    results.sort(key=lambda x: x["score"], reverse=True)

    return results
