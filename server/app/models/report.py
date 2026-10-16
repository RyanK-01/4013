"""SQLAlchemy ORM models for user-submitted reports: bugs, feature suggestions, and incorrect info."""

import datetime
from sqlalchemy import String, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class BugReport(Base):
    """User-reported application bug categorised by type (UI Bug, Data Error, etc.)."""
    __tablename__ = "bug_reports"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    category: Mapped[str] = mapped_column(String(100), nullable=False)  # e.g. "UI Bug", "Data Error", "Others"
    description: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="pending")  # pending, reviewed, resolved
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    user = relationship("User", back_populates="bug_reports")


class FeatureSuggestion(Base):
    """User-submitted idea for a new feature or improvement."""

    __tablename__ = "feature_suggestions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="pending")  # pending, reviewed, implemented
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    user = relationship("User", back_populates="feature_suggestions")


class IncorrectInfoReport(Base):
    """Report flagging incorrect stall data such as wrong hours, prices, or closure status."""

    __tablename__ = "incorrect_info_reports"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    stall_id: Mapped[int] = mapped_column(ForeignKey("stalls.id", ondelete="CASCADE"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    issue_type: Mapped[str] = mapped_column(String(100), nullable=False)  # "Wrong Hours", "Wrong Price", "Closed", "Others"
    description: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="pending")  # pending, reviewed, resolved
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    user = relationship("User", back_populates="incorrect_info_reports")
