"""
Stall Schemas  (<<datatype>>)

Pydantic models for stall CRUD: creation, partial update, full detail response,
lightweight list response, plus menu item and dietary tag sub-schemas.
"""

from pydantic import BaseModel
from datetime import datetime


class MenuItemCreate(BaseModel):
    """Menu item input — name, optional price and description."""
    # TODO: define name (str), price (float|None), description (str|None)
    pass


class MenuItemOut(BaseModel):
    """Menu item response with id and image_url."""
    # TODO: define id, name, price, description, image_url
    pass


class StallCreate(BaseModel):
    """New stall submission — includes address, cuisine, prices, tags, menu items."""
    # TODO: define name, description, address, lat/lng, cuisine_type, price range,
    #       operating_hours, indoor_outdoor, dietary_tags list, menu_items list
    pass


class StallUpdate(BaseModel):
    """Partial update — all fields optional so only changed fields are sent."""
    # TODO: same fields as StallCreate but all Optional
    pass


class DietaryTagOut(BaseModel):
    """Dietary tag response — id and tag string."""
    # TODO: define id, tag
    pass


class StallOut(BaseModel):
    """Full stall detail with nested menu items, dietary tags, and computed distance."""
    # TODO: define all stall fields + dietary_tags list + menu_items list + distance (optional)
    pass


class StallListOut(BaseModel):
    """Lightweight stall summary for search results and list views."""
    # TODO: define id, name, address, cuisine_type, price range, rating, image, crowd, distance
    pass
