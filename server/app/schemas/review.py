"""Pydantic schemas for creating and returning stall reviews."""

from pydantic import BaseModel
from datetime import datetime


class ReviewCreate(BaseModel):
    """Request body for submitting a new review (photo uploaded separately as form data)."""
    stall_id: int
    rating: float  # 1-5
    comment: str | None = None


class ReviewOut(BaseModel):
    """Review data returned in API responses, including approval status."""
    id: int
    stall_id: int
    user_id: int
    rating: float
    comment: str | None
    photo_url: str
    is_approved: bool
    created_at: datetime
    username: str | None = None

    model_config = {"from_attributes": True}
