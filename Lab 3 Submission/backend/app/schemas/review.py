"""
Review Schemas  (<<datatype>>)

Pydantic models for submitting reviews (with photo as separate form upload)
and returning review data including approval status and author username.
"""

from pydantic import BaseModel
from datetime import datetime


class ReviewCreate(BaseModel):
    """Review submission — stall_id, rating (1-5), optional comment. Photo uploaded separately."""
    # TODO: define stall_id (int), rating (float), comment (str|None)
    pass


class ReviewOut(BaseModel):
    """Review response with approval status and author's username."""
    # TODO: define id, stall_id, user_id, rating, comment, photo_url, is_approved, created_at, username
    pass
