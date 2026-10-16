"""API route for retrieving the current user's favourite stalls."""

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
def get_favourites(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Return all approved stalls the current user has favourited, newest first. Requires JWT."""
    favs = (
        db.query(Stall)
        .join(Favourite, Favourite.stall_id == Stall.id)
        .filter(Favourite.user_id == current_user.id, Stall.is_approved == True)
        .order_by(Favourite.created_at.desc())
        .all()
    )
    return favs
