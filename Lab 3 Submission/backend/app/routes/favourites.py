"""
Favourites Route  (<<boundary>>)

Returns the list of stalls the current user has bookmarked.
The actual toggle/check endpoints live under /api/stalls/{id}/favourite.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.favourite import Favourite
from app.models.stall import Stall
from app.schemas.stall import StallListOut
from app.middleware.auth import get_current_user

router = APIRouter(prefix="/api/favourites", tags=["favourites"])


@router.get("/", response_model=list[StallListOut])
def get_favourites(db: Session = Depends(get_db),
                   current_user: User = Depends(get_current_user)):
    """Return all approved stalls the current user has favourited, newest first."""
    # TODO: join Stall with Favourite on stall_id, filter by current user, order by date
    pass
