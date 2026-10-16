"""
Review Routes  (<<boundary>>)

Handles review submission (with required photo upload as multipart form)
and retrieval of the current user's review history.
"""

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.review import Review
from app.models.user import User
from app.schemas.review import ReviewOut
from app.middleware.auth import get_current_user

router = APIRouter(prefix="/api/reviews", tags=["reviews"])


@router.post("/", response_model=ReviewOut)
async def create_review(stall_id: int = Form(...), rating: float = Form(...),
                        comment: str = Form(None), photo: UploadFile = File(...),
                        db: Session = Depends(get_db),
                        current_user: User = Depends(get_current_user)):
    """Submit a review with a required food photo (multipart form, requires JWT)."""
    # TODO: validate photo is an image, save to uploads dir, create Review (is_approved=False)
    pass


@router.get("/my", response_model=list[ReviewOut])
def get_my_reviews(db: Session = Depends(get_db),
                   current_user: User = Depends(get_current_user)):
    """List all reviews submitted by the current user, newest first (requires JWT)."""
    # TODO: query reviews where user_id = current_user.id, order by created_at desc
    pass
