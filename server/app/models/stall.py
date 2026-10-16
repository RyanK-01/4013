"""SQLAlchemy ORM models for hawker food stalls and related entities."""

import datetime
from sqlalchemy import String, Float, Integer, Boolean, Text, DateTime, ForeignKey, func, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class CuisineType(Base):
    """Lookup table of distinct cuisine categories (e.g. Chinese, Malay, Indian)."""
    __tablename__ = "cuisine_types"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)


class StallDietaryTag(Base):
    """Many-to-many association between stalls and dietary labels (e.g. Halal, Vegetarian)."""

    __tablename__ = "stall_dietary_tags"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    stall_id: Mapped[int] = mapped_column(ForeignKey("stalls.id", ondelete="CASCADE"), nullable=False)
    tag: Mapped[str] = mapped_column(String(100), nullable=False)  # e.g. "Halal", "Vegetarian", "No Seafood"

    stall = relationship("Stall", back_populates="dietary_tags")


class Stall(Base):
    """Represents a hawker food stall with location, pricing, and approval status.

    Stalls can be seeded from data.gov.sg or submitted by users (pending admin approval).
    """

    __tablename__ = "stalls"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    address: Mapped[str] = mapped_column(String(500), nullable=False)
    latitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    longitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    cuisine_type: Mapped[str | None] = mapped_column(String(100), nullable=True)
    price_range_min: Mapped[float | None] = mapped_column(Float, nullable=True)
    price_range_max: Mapped[float | None] = mapped_column(Float, nullable=True)
    operating_hours: Mapped[dict | None] = mapped_column(JSON, nullable=True)  # {"mon": "08:00-20:00", ...}
    indoor_outdoor: Mapped[str | None] = mapped_column(String(20), nullable=True)  # "Indoor", "Outdoor"
    image_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    google_rating: Mapped[float | None] = mapped_column(Float, nullable=True)
    google_review_count: Mapped[int | None] = mapped_column(Integer, nullable=True)

    # Approval workflow
    is_approved: Mapped[bool] = mapped_column(Boolean, default=False)
    submitted_by: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    rejection_reason: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Crowd level (approved aggregate)
    crowd_level: Mapped[int | None] = mapped_column(Integer, nullable=True)  # 0-100 percentage

    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    dietary_tags = relationship("StallDietaryTag", back_populates="stall", cascade="all, delete-orphan")
    menu_items = relationship("MenuItem", back_populates="stall", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="stall", cascade="all, delete-orphan")
    favourites = relationship("Favourite", back_populates="stall", cascade="all, delete-orphan")
    crowd_reports = relationship("CrowdReport", back_populates="stall", cascade="all, delete-orphan")


class MenuItem(Base):
    """Individual dish or drink offered by a stall, with optional price and image."""

    __tablename__ = "menu_items"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    stall_id: Mapped[int] = mapped_column(ForeignKey("stalls.id", ondelete="CASCADE"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    price: Mapped[float | None] = mapped_column(Float, nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    image_url: Mapped[str | None] = mapped_column(String(500), nullable=True)

    stall = relationship("Stall", back_populates="menu_items")
