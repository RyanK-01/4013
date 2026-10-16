"""Pydantic schemas for stall CRUD operations, menu items, and dietary tags."""

from pydantic import BaseModel
from datetime import datetime


class MenuItemCreate(BaseModel):
    """Request body for adding a menu item to a stall."""
    name: str
    price: float | None = None
    description: str | None = None


class MenuItemOut(BaseModel):
    """Menu item data returned in API responses."""
    id: int
    name: str
    price: float | None
    description: str | None
    image_url: str | None

    model_config = {"from_attributes": True}


class StallCreate(BaseModel):
    """Request body for submitting a new stall (subject to admin approval)."""
    name: str
    description: str | None = None
    address: str
    latitude: float | None = None
    longitude: float | None = None
    cuisine_type: str | None = None
    price_range_min: float | None = None
    price_range_max: float | None = None
    operating_hours: dict | None = None
    indoor_outdoor: str | None = None
    dietary_tags: list[str] = []
    menu_items: list[MenuItemCreate] = []


class StallUpdate(BaseModel):
    """Partial-update schema for editing stall details (all fields optional)."""
    name: str | None = None
    description: str | None = None
    address: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    cuisine_type: str | None = None
    price_range_min: float | None = None
    price_range_max: float | None = None
    operating_hours: dict | None = None
    indoor_outdoor: str | None = None
    dietary_tags: list[str] | None = None


class DietaryTagOut(BaseModel):
    """Dietary tag data returned in API responses."""
    id: int
    tag: str

    model_config = {"from_attributes": True}


class StallOut(BaseModel):
    """Full stall detail returned for single-stall views, including nested menu items and tags."""
    id: int
    name: str
    description: str | None
    address: str
    latitude: float | None
    longitude: float | None
    cuisine_type: str | None
    price_range_min: float | None
    price_range_max: float | None
    operating_hours: dict | None
    indoor_outdoor: str | None
    image_url: str | None
    google_rating: float | None
    google_review_count: int | None
    is_approved: bool
    crowd_level: int | None
    dietary_tags: list[DietaryTagOut] = []
    menu_items: list[MenuItemOut] = []
    created_at: datetime
    distance: float | None = None  # computed field for proximity results

    model_config = {"from_attributes": True}


class StallListOut(BaseModel):
    """Lightweight stall summary used in list/search result views."""
    id: int
    name: str
    address: str
    cuisine_type: str | None
    price_range_min: float | None
    price_range_max: float | None
    google_rating: float | None
    image_url: str | None
    crowd_level: int | None
    is_approved: bool
    distance: float | None = None

    model_config = {"from_attributes": True}
