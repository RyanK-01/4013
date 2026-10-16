"""
Review Entity  (<<entity>>)

User-submitted review of a stall with mandatory photo upload,
star rating (1.0–5.0), and optional text comment.
Reviews require admin approval before they appear publicly.
"""

from sqlalchemy import Float, Text, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Review(Base):
    __tablename__ = "reviews"

    # TODO: define columns — id (pk), stall_id (fk → stalls), user_id (fk → users),
    #       rating (float), comment (text, nullable), photo_url (str),
    #       is_approved (default False), rejection_reason, created_at
    pass
