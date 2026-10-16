"""SQLAlchemy ORM model for user-favourited stalls."""

import datetime
from sqlalchemy import Integer, DateTime, ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Favourite(Base):
    """Tracks a user's bookmarked stalls. Each user–stall pair is unique."""
    __tablename__ = "favourites"
    __table_args__ = (UniqueConstraint("user_id", "stall_id", name="uq_user_stall_fav"),)

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    stall_id: Mapped[int] = mapped_column(ForeignKey("stalls.id", ondelete="CASCADE"), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    user = relationship("User", back_populates="favourites")
    stall = relationship("Stall", back_populates="favourites")
