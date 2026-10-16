"""API route for generating personalised stall recommendations."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.recommendation import FilterSelection
from app.schemas.stall import StallOut
from app.middleware.auth import get_current_user, get_optional_user
from app.services.recommendation import get_recommendations

router = APIRouter(prefix="/api/recommendations", tags=["recommendations"])


@router.post("/", response_model=list[StallOut])
def generate_recommendations(
    filters: FilterSelection,
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_optional_user),
):
    """Generate ranked stall recommendations based on user-selected filters.

    Accepts budget, dietary, proximity, and popularity preferences.
    Optionally boosts results for authenticated users based on their favourites.
    """
    user_id = current_user.id if current_user else None
    results = get_recommendations(db, filters, user_id=user_id)

    stall_list = []
    for r in results:
        stall = r["stall"]
        stall_out = StallOut.model_validate(stall)
        stall_out.distance = r.get("distance")
        stall_list.append(stall_out)

    return stall_list
