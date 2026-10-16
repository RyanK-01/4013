"""OneMap API integration for Singapore geocoding and routing.

Provides address search, reverse geocoding, and point-to-point routing via
the Singapore Land Authority's OneMap REST API. Token is auto-renewed (3-day TTL).
Docs: https://www.onemap.gov.sg/apidocs/
"""

import httpx
import logging
from datetime import datetime, timezone

from app.config import settings

logger = logging.getLogger(__name__)

ONEMAP_BASE = "https://www.onemap.gov.sg"
ONEMAP_SEARCH = f"{ONEMAP_BASE}/api/common/elastic/search"
ONEMAP_REVERSE_GEOCODE = f"{ONEMAP_BASE}/api/public/revgeocode"
ONEMAP_ROUTE = f"{ONEMAP_BASE}/api/public/routingSvc"
ONEMAP_AUTH = f"{ONEMAP_BASE}/api/auth/post/getToken"

# Module-level token cache
_cached_token: str | None = None
_token_expiry: datetime | None = None


async def _get_token() -> str | None:
    """Return a cached OneMap token or authenticate for a fresh one. Returns None if credentials are missing."""
    global _cached_token, _token_expiry

    if not settings.ONEMAP_EMAIL or not settings.ONEMAP_PASSWORD:
        return None

    if _cached_token and _token_expiry and datetime.now(timezone.utc) < _token_expiry:
        return _cached_token

    try:
        async with httpx.AsyncClient(timeout=15) as client:
            resp = await client.post(
                ONEMAP_AUTH,
                json={
                    "email": settings.ONEMAP_EMAIL,
                    "password": settings.ONEMAP_PASSWORD,
                },
            )
            resp.raise_for_status()
            data = resp.json()
            _cached_token = data.get("access_token")
            expiry_str = data.get("expiry_timestamp")
            if expiry_str:
                _token_expiry = datetime.fromisoformat(expiry_str)
            logger.info("OneMap token refreshed")
            return _cached_token
    except Exception as e:
        logger.warning("OneMap auth failed: %s", e)
        return None


async def search_address(query: str, page: int = 1) -> list[dict]:
    """
    Search for an address/place in Singapore using OneMap.
    Returns list of results with lat, lng, address, building name, postal code.
    """
    token = await _get_token()
    if not token:
        logger.warning("OneMap token unavailable – search skipped")
        return []

    try:
        async with httpx.AsyncClient(timeout=15) as client:
            resp = await client.get(
                ONEMAP_SEARCH,
                params={
                    "searchVal": query,
                    "returnGeom": "Y",
                    "getAddrDetails": "Y",
                    "pageNum": page,
                },
                headers={"Authorization": f"Bearer {token}"},
            )
            resp.raise_for_status()
            data = resp.json()

        results = []
        for item in data.get("results", []):
            results.append({
                "address": item.get("ADDRESS"),
                "building": item.get("BUILDING"),
                "postal_code": item.get("POSTAL"),
                "latitude": float(item["LATITUDE"]) if item.get("LATITUDE") else None,
                "longitude": float(item["LONGITUDE"]) if item.get("LONGITUDE") else None,
            })
        return results

    except Exception as e:
        logger.warning("OneMap search error: %s", e)
        return []


async def reverse_geocode(lat: float, lng: float) -> dict | None:
    """
    Convert coordinates to a Singapore address using OneMap.
    """
    token = await _get_token()
    if not token:
        return None

    try:
        async with httpx.AsyncClient(timeout=15) as client:
            resp = await client.get(
                ONEMAP_REVERSE_GEOCODE,
                params={
                    "location": f"{lat},{lng}",
                    "buffer": 200,
                    "addressType": "All",
                },
                headers={"Authorization": f"Bearer {token}"},
            )
            resp.raise_for_status()
            data = resp.json()

        results = data.get("GeocodeInfo", [])
        if results:
            first = results[0]
            return {
                "address": first.get("ROAD") or first.get("BUILDINGNAME"),
                "building": first.get("BUILDINGNAME"),
                "block": first.get("BLOCK"),
                "postal_code": first.get("POSTALCODE"),
            }
        return None

    except Exception as e:
        logger.warning("OneMap reverse geocode error: %s", e)
        return None


async def get_route(
    start_lat: float, start_lng: float,
    end_lat: float, end_lng: float,
    route_type: str = "walk",
) -> dict | None:
    """
    Get route between two points using OneMap routing.
    route_type: 'walk', 'drive', 'pt' (public transport), 'cycle'
    """
    token = await _get_token()
    if not token:
        return None

    try:
        async with httpx.AsyncClient(timeout=15) as client:
            resp = await client.get(
                ONEMAP_ROUTE,
                params={
                    "start": f"{start_lat},{start_lng}",
                    "end": f"{end_lat},{end_lng}",
                    "routeType": route_type,
                },
                headers={"Authorization": f"Bearer {token}"},
            )
            resp.raise_for_status()
            data = resp.json()

        if "route_summary" in data:
            return {
                "total_distance_m": data["route_summary"].get("total_distance"),
                "total_time_s": data["route_summary"].get("total_time"),
                "route_geometry": data.get("route_geometry"),
                "route_instructions": data.get("route_instructions"),
            }
        return None

    except Exception as e:
        logger.warning("OneMap routing error: %s", e)
        return None
