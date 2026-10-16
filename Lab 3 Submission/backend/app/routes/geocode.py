"""
Geocoding Routes  (<<boundary>>)

Thin wrapper around the OneMap service for the frontend.
Provides address search, reverse geocoding (coords → address),
and walking/driving/cycling/PT routing between two points.
"""

from fastapi import APIRouter, Query

from app.services.onemap import search_address, reverse_geocode, get_route

router = APIRouter(prefix="/api/geocode", tags=["geocode"])


@router.get("/search")
async def geocode_search(q: str = Query(..., min_length=2)):
    """Search for a Singapore address/place by keyword."""
    # TODO: call search_address service
    pass


@router.get("/reverse")
async def geocode_reverse(lat: float = Query(...), lng: float = Query(...)):
    """Convert GPS coordinates to a Singapore address."""
    # TODO: call reverse_geocode service
    pass


@router.get("/route")
async def geocode_route(start_lat: float = Query(...), start_lng: float = Query(...),
                        end_lat: float = Query(...), end_lng: float = Query(...),
                        mode: str = Query("walk")):
    """Get route between two points. Modes: walk, drive, pt, cycle."""
    # TODO: call get_route service
    pass
