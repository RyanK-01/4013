"""API routes for submitting and retrieving stall reviews."""

import os
import uuid
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.models.review import Review
from app.models.user import User
from app.schemas.review import ReviewOut
from app.middleware.auth import get_current_user

router = APIRouter(prefix="/api/reviews", tags=["reviews"])


@router.post("/", response_model=ReviewOut)
async def create_review(
    stall_id: int = Form(...),
    rating: float = Form(...),
    comment: str = Form(None),
    photo: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Submit a new review with a required photo. Requires JWT.

    Saves the uploaded image to disk and creates a review pending admin approval.
    Accepts multipart form data (stall_id, rating, comment, photo).
    """
    if not photo.content_type or not photo.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="A photo is required for reviews")

    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    ext = photo.filename.split(".")[-1] if photo.filename else "jpg"
    filename = f"{uuid.uuid4()}.{ext}"
    filepath = os.path.join(settings.UPLOAD_DIR, filename)

    content = await photo.read()
    with open(filepath, "wb") as f:
        f.write(content)

    review = Review(
        stall_id=stall_id,
        user_id=current_user.id,
        rating=rating,
        comment=comment,
        photo_url=f"/uploads/{filename}",
        is_approved=False,
    )
    db.add(review)
    db.commit()
    db.refresh(review)

    out = ReviewOut.model_validate(review)
    out.username = current_user.username
    return out


@router.get("/my", response_model=list[ReviewOut])
def get_my_reviews(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """List all reviews submitted by the current user, newest first. Requires JWT."""
    reviews = (
        db.query(Review)
        .filter(Review.user_id == current_user.id)
        .order_by(Review.created_at.desc())
        .all()
    )
    return [ReviewOut.model_validate(r) for r in reviews]
