"""
Recommendation Routes  (<<boundary>>)

Accepts filter preferences from the client and returns a ranked list
of stall recommendations. Works for both anonymous and logged-in users
(logged-in users get favourites boosting).
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.recommendation import FilterSelection
from app.schemas.stall import StallOut
from app.middleware.auth import get_optional_user
from app.services.recommendation import get_recommendations

router = APIRouter(prefix="/api/recommendations", tags=["recommendations"])


@router.post("/", response_model=list[StallOut])
def generate_recommendations(filters: FilterSelection, db: Session = Depends(get_db),
                             current_user: User | None = Depends(get_optional_user)):
    """Generate ranked stall recommendations from the given filters."""
    # TODO: call get_recommendations service, convert results to StallOut list with distance
    pass
