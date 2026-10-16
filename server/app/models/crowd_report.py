"""SQLAlchemy ORM model for user-submitted crowd-level reports."""

import datetime
from sqlalchemy import Integer, Boolean, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class CrowdReport(Base):
    """User-reported crowd level (0–100 %) for a stall, subject to admin approval."""
    __tablename__ = "crowd_reports"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    stall_id: Mapped[int] = mapped_column(ForeignKey("stalls.id", ondelete="CASCADE"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    crowd_level: Mapped[int] = mapped_column(Integer, nullable=False)  # 0-100 percentage
    is_approved: Mapped[bool] = mapped_column(Boolean, default=False)
    rejection_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    stall = relationship("Stall", back_populates="crowd_reports")
    user = relationship("User", back_populates="crowd_reports")
