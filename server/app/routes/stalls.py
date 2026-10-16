"""API routes for hawker stall discovery, browsing, and user submissions."""

import os
from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.models.stall import Stall, MenuItem, StallDietaryTag, CuisineType
from app.models.review import Review
from app.models.favourite import Favourite
from app.models.user import User
from app.schemas.stall import StallCreate, StallUpdate, StallOut, StallListOut, MenuItemCreate
from app.schemas.review import ReviewOut
from app.middleware.auth import get_current_user, get_optional_user
from app.services.location import haversine_distance

router = APIRouter(prefix="/api/stalls", tags=["stalls"])


@router.get("/", response_model=list[StallListOut])
def list_stalls(
    search: str | None = None,
    cuisine: str | None = None,
    limit: int = Query(50, le=100),
    offset: int = 0,
    db: Session = Depends(get_db),
):
    """List approved stalls with optional search and cuisine filters.

    Supports text search across name, cuisine, and address fields.
    Results are ordered by Google rating descending.
    """
    query = db.query(Stall).filter(Stall.is_approved == True)

    if search:
        search_term = f"%{search}%"
        query = query.filter(
            (Stall.name.ilike(search_term))
            | (Stall.cuisine_type.ilike(search_term))
            | (Stall.address.ilike(search_term))
        )

    if cuisine:
        query = query.filter(Stall.cuisine_type.ilike(f"%{cuisine}%"))

    stalls = query.order_by(Stall.google_rating.desc().nullslast()).offset(offset).limit(limit).all()
    return stalls


@router.get("/nearby", response_model=list[StallListOut])
def get_nearby_stalls(
    lat: float = Query(...),
    lng: float = Query(...),
    radius_km: float = Query(5.0, le=30.0),
    limit: int = Query(20, le=50),
    db: Session = Depends(get_db),
):
    """Find approved stalls within a given radius of the user's coordinates.

    Uses Haversine distance. Results sorted by proximity, closest first.
    """
    stalls = db.query(Stall).filter(
        Stall.is_approved == True,
        Stall.latitude.isnot(None),
        Stall.longitude.isnot(None),
    ).all()

    nearby = []
    for stall in stalls:
        dist = haversine_distance(lat, lng, stall.latitude, stall.longitude)
        if dist <= radius_km:
            stall_dict = StallListOut.model_validate(stall)
            stall_dict.distance = round(dist, 2)
            nearby.append(stall_dict)

    nearby.sort(key=lambda s: s.distance or 999)
    return nearby[:limit]


@router.get("/categories")
def get_categories(db: Session = Depends(get_db)):
    """Return all cuisine category names. Falls back to defaults if none exist in DB."""
    cuisines = db.query(CuisineType).order_by(CuisineType.name).all()
    if not cuisines:
        # Return default categories
        return [
            "Chinese Cuisine", "Malay Cuisine", "Indian Cuisine",
            "Western", "Seafood", "Japanese", "Korean", "Thai",
            "Halal", "Vegetarian", "Desserts", "Drinks",
        ]
    return [c.name for c in cuisines]


@router.get("/browse/{category}", response_model=list[StallListOut])
def browse_by_category(
    category: str,
    lat: float | None = None,
    lng: float | None = None,
    limit: int = Query(10, le=30),
    db: Session = Depends(get_db),
):
    """Browse approved stalls by cuisine category.

    Optionally accepts user coordinates to compute distance and cap at 30 km.
    """
    query = db.query(Stall).filter(
        Stall.is_approved == True,
        Stall.cuisine_type.ilike(f"%{category}%"),
    )
    stalls = query.all()

    results = []
    for stall in stalls:
        stall_out = StallListOut.model_validate(stall)
        if lat and lng and stall.latitude and stall.longitude:
            dist = haversine_distance(lat, lng, stall.latitude, stall.longitude)
            if dist <= 30.0:
                stall_out.distance = round(dist, 2)
                results.append(stall_out)
        else:
            results.append(stall_out)

    results.sort(key=lambda s: s.distance if s.distance is not None else 999)
    return results[:limit]


@router.get("/{stall_id}", response_model=StallOut)
def get_stall(stall_id: int, db: Session = Depends(get_db)):
    """Retrieve full details of a single approved stall by ID."""
    stall = db.query(Stall).filter(Stall.id == stall_id, Stall.is_approved == True).first()
    if not stall:
        raise HTTPException(status_code=404, detail="Stall not found")
    return stall


@router.get("/{stall_id}/reviews", response_model=list[ReviewOut])
def get_stall_reviews(stall_id: int, db: Session = Depends(get_db)):
    """List all approved reviews for a stall, newest first."""
    reviews = (
        db.query(Review)
        .filter(Review.stall_id == stall_id, Review.is_approved == True)
        .order_by(Review.created_at.desc())
        .all()
    )
    result = []
    for r in reviews:
        out = ReviewOut.model_validate(r)
        out.username = r.user.username if r.user else None
        result.append(out)
    return result


@router.post("/submit", response_model=StallOut)
def submit_new_stall(
    data: StallCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Submit a new stall for admin approval. Requires JWT.

    Creates the stall with is_approved=False, along with dietary tags and menu items.
    """
    stall = Stall(
        name=data.name,
        description=data.description,
        address=data.address,
        latitude=data.latitude,
        longitude=data.longitude,
        cuisine_type=data.cuisine_type,
        price_range_min=data.price_range_min,
        price_range_max=data.price_range_max,
        operating_hours=data.operating_hours,
        indoor_outdoor=data.indoor_outdoor,
        is_approved=False,
        submitted_by=current_user.id,
    )
    db.add(stall)
    db.flush()

    for tag_name in data.dietary_tags:
        tag = StallDietaryTag(stall_id=stall.id, tag=tag_name)
        db.add(tag)

    for item in data.menu_items:
        menu_item = MenuItem(
            stall_id=stall.id,
            name=item.name,
            price=item.price,
            description=item.description,
        )
        db.add(menu_item)

    db.commit()
    db.refresh(stall)
    return stall


# ── Favourites ──

@router.post("/{stall_id}/favourite")
def toggle_favourite(
    stall_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Toggle a stall as favourite for the current user. Requires JWT."""
    existing = (
        db.query(Favourite)
        .filter(Favourite.user_id == current_user.id, Favourite.stall_id == stall_id)
        .first()
    )
    if existing:
        db.delete(existing)
        db.commit()
        return {"status": "removed", "is_favourite": False}

    fav = Favourite(user_id=current_user.id, stall_id=stall_id)
    db.add(fav)
    db.commit()
    return {"status": "added", "is_favourite": True}


@router.get("/{stall_id}/is-favourite")
def check_favourite(
    stall_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Check whether the current user has favourited a stall. Requires JWT."""
    existing = (
        db.query(Favourite)
        .filter(Favourite.user_id == current_user.id, Favourite.stall_id == stall_id)
        .first()
    )
    return {"is_favourite": existing is not None}
