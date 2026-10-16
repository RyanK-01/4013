"""
Stall, MenuItem, StallDietaryTag, CuisineType Entities  (<<entity>>)

Core domain models for hawker food stalls and their associated data.
Stalls go through an approval workflow (is_approved flag) before
becoming visible to regular users. Each stall has a cuisine type,
optional dietary tags, menu items, and user-generated crowd level data.
"""

from sqlalchemy import String, Float, Integer, Boolean, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class CuisineType(Base):
    __tablename__ = "cuisine_types"

    # TODO: define columns — id (pk), name (unique)
    pass


class StallDietaryTag(Base):
    __tablename__ = "stall_dietary_tags"

    # TODO: define columns — id (pk), stall_id (fk → stalls), tag (str)
    pass


class Stall(Base):
    __tablename__ = "stalls"

    # TODO: define columns — id (pk), name, description, address, latitude, longitude,
    #       cuisine_type, image_url, avg_price_min, avg_price_max, rating_avg, review_count,
    #       operating_hours, indoor_outdoor, crowd_level, is_approved, rejection_reason,
    #       submitted_by (fk → users), gov_synced (bool), created_at
    pass


class MenuItem(Base):
    __tablename__ = "menu_items"

    # TODO: define columns — id (pk), stall_id (fk → stalls), name, price, description, image_url
    pass
