"""
Geocoding routes – wraps OneMap API for the frontend.
Falls back gracefully when OneMap credentials are not configured.
"""
from fastapi import APIRouter, Query

from app.services.onemap import search_address, reverse_geocode, get_route

router = APIRouter(prefix="/api/geocode", tags=["geocode"])


@router.get("/search")
async def geocode_search(q: str = Query(..., min_length=2)):
    """
    Search for a Singapore address using OneMap.
    Returns a list of matching results with coordinates.
    """
    results = await search_address(q)
    if not results:
        return {"results": [], "source": "onemap", "note": "No results or OneMap unavailable"}
    return {"results": results, "source": "onemap"}


@router.get("/reverse")
async def geocode_reverse(lat: float = Query(...), lng: float = Query(...)):
    """
    Convert coordinates to a Singapore address using OneMap.
    """
    result = await reverse_geocode(lat, lng)
    if not result:
        return {"result": None, "source": "onemap", "note": "No result or OneMap unavailable"}
    return {"result": result, "source": "onemap"}


@router.get("/route")
async def geocode_route(
    start_lat: float = Query(...),
    start_lng: float = Query(...),
    end_lat: float = Query(...),
    end_lng: float = Query(...),
    mode: str = Query("walk"),
):
    """
    Get routing information between two points in Singapore.
    mode: walk, drive, pt (public transport), cycle
    """
    result = await get_route(start_lat, start_lng, end_lat, end_lng, route_type=mode)
    if not result:
        return {"route": None, "source": "onemap", "note": "No route or OneMap unavailable"}
    return {"route": result, "source": "onemap"}
