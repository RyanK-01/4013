"""
Stall Routes  (<<boundary>>)

Public endpoints for stall discovery: list/search, nearby (GPS radius),
browse by cuisine, full detail, reviews. Authenticated endpoints for (admin)
submitting new stalls and managing favourites.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.stall import Stall, MenuItem, StallDietaryTag, CuisineType
from app.models.review import Review
from app.models.favourite import Favourite
from app.models.user import User
from app.schemas.stall import StallCreate, StallOut, StallListOut
from app.schemas.review import ReviewOut
from app.middleware.auth import get_current_user, get_optional_user
from app.services.location import haversine_distance

router = APIRouter(prefix="/api/stalls", tags=["stalls"])


@router.get("/", response_model=list[StallListOut])
def list_stalls(search: str | None = None, cuisine: str | None = None,
                limit: int = Query(50, le=100), offset: int = 0,
                db: Session = Depends(get_db)):
    """List approved stalls with optional text search and cuisine filter."""
    # TODO: query approved stalls, apply ilike search on name/cuisine/address, order by rating
    pass


@router.get("/nearby", response_model=list[StallListOut])
def get_nearby_stalls(lat: float = Query(...), lng: float = Query(...),
                      radius_km: float = Query(5.0, le=30.0),
                      limit: int = Query(20, le=50),
                      db: Session = Depends(get_db)):
    """Find approved stalls within a radius using Haversine distance, sorted by proximity."""
    # TODO: compute haversine distance for each stall, filter by radius, sort closest first
    pass


@router.get("/categories")
def get_categories(db: Session = Depends(get_db)):
    """Return all cuisine category names from the CuisineType table."""
    # TODO: query CuisineType table, fall back to hardcoded defaults if empty
    pass


@router.get("/browse/{category}", response_model=list[StallListOut])
def browse_by_category(category: str, lat: float | None = None, lng: float | None = None,
                       limit: int = Query(10, le=30), db: Session = Depends(get_db)):
    """Browse approved stalls by cuisine category, optionally with distance."""
    # TODO: filter by cuisine_type, compute distance if coords provided, cap at 30 km
    pass


@router.get("/{stall_id}", response_model=StallOut)
def get_stall(stall_id: int, db: Session = Depends(get_db)):
    """Get full details of a single approved stall by ID."""
    # TODO: query stall by id, return 404 if not found or not approved
    pass


@router.get("/{stall_id}/reviews", response_model=list[ReviewOut])
def get_stall_reviews(stall_id: int, db: Session = Depends(get_db)):
    """List all approved reviews for a stall, newest first."""
    # TODO: query approved reviews for this stall, include reviewer username
    pass


@router.post("/submit", response_model=StallOut)
def submit_new_stall(data: StallCreate, db: Session = Depends(get_db),
                     current_user: User = Depends(get_current_user)):
    """Submit a new stall for admin approval (requires JWT)."""
    # TODO: create Stall with is_approved=False, add dietary tags and menu items
    pass


@router.post("/{stall_id}/favourite")
def toggle_favourite(stall_id: int, db: Session = Depends(get_db),
                     current_user: User = Depends(get_current_user)):
    """Toggle favourite on a stall — add if not favourited, remove if already (requires JWT)."""
    # TODO: check if Favourite exists, delete if yes, create if no
    pass


@router.get("/{stall_id}/is-favourite")
def check_favourite(stall_id: int, db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    """Check whether the current user has favourited this stall (requires JWT)."""
    # TODO: query Favourite table, return {"is_favourite": bool}
    pass
