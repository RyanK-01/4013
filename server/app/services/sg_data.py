"""Integration with data.gov.sg for importing hawker centre data.

Fetches from two NEA-sourced datasets and merges them by centre name:

  1. Hawker List (CSV/JSON) – centre metadata, stall counts, ownership.
     Resource: d_68a42f09f350881996d83f9cd73ab02f

  2. Hawker GeoJSON – coordinates, addresses, photos, status.
     Dataset: d_4a086da0a5553be1d89383cd90d07ecd (poll-download → S3 signed URL)
"""

import httpx
import logging
from typing import Any

logger = logging.getLogger(__name__)

# ── data.gov.sg resource IDs ──
HAWKER_LIST_RESOURCE = "d_68a42f09f350881996d83f9cd73ab02f"
HAWKER_GEOJSON_DATASET = "d_4a086da0a5553be1d89383cd90d07ecd"

DATAGOVSG_SEARCH_URL = "https://data.gov.sg/api/action/datastore_search"
DATAGOVSG_POLL_URL = (
    "https://api-open.data.gov.sg/v1/public/api/datasets/{dataset_id}/poll-download"
)


async def fetch_hawker_list() -> list[dict[str, Any]]:
    """
    Fetch all hawker centres from data.gov.sg CSV dataset.
    Returns list of dicts with keys:
        name_of_centre, location_of_centre, type_of_centre,
        owner, no_of_stalls, no_of_cooked_food_stalls, no_of_mkt_produce_stalls
    """
    import asyncio

    records: list[dict] = []
    offset = 0
    limit = 200  # fetch all in one request to avoid rate limits

    async with httpx.AsyncClient(timeout=30) as client:
        while True:
            resp = await client.get(
                DATAGOVSG_SEARCH_URL,
                params={
                    "resource_id": HAWKER_LIST_RESOURCE,
                    "limit": limit,
                    "offset": offset,
                },
            )
            if resp.status_code == 429:
                logger.warning("Rate limited by data.gov.sg, waiting 3s...")
                await asyncio.sleep(3)
                continue
            resp.raise_for_status()
            data = resp.json()

            result = data.get("result", {})
            batch = result.get("records", [])
            records.extend(batch)

            total = result.get("total", 0)
            offset += limit
            if offset >= total:
                break
            await asyncio.sleep(1)  # be polite to the API

    logger.info("Fetched %d hawker centres from data.gov.sg list", len(records))
    return records


async def fetch_hawker_geojson() -> dict[str, Any]:
    """
    Fetch the Hawker Centres GeoJSON from data.gov.sg.
    Returns the full FeatureCollection dict.
    """
    async with httpx.AsyncClient(timeout=30, follow_redirects=True) as client:
        # Step 1 – get signed download URL
        poll_resp = await client.get(
            DATAGOVSG_POLL_URL.format(dataset_id=HAWKER_GEOJSON_DATASET)
        )
        poll_resp.raise_for_status()
        poll_data = poll_resp.json()

        if poll_data.get("code") != 0:
            raise RuntimeError(f"data.gov.sg poll error: {poll_data.get('errorMsg')}")

        download_url = poll_data["data"]["url"]

        # Step 2 – download actual GeoJSON
        geo_resp = await client.get(download_url)
        geo_resp.raise_for_status()
        geojson = geo_resp.json()

    features = geojson.get("features", [])
    logger.info("Fetched %d features from Hawker Centres GeoJSON", len(features))
    return geojson


def merge_hawker_data(
    hawker_list: list[dict], geojson: dict
) -> list[dict[str, Any]]:
    """
    Merge the CSV list with GeoJSON features by matching on centre name.
    If CSV list is empty, falls back to building records from GeoJSON alone.
    Returns enriched list of hawker centre dicts ready for DB insertion.
    """

    # Build a lookup from GeoJSON by name (normalised)
    geo_lookup: dict[str, dict] = {}
    for feature in geojson.get("features", []):
        props = feature.get("properties", {})
        coords = feature.get("geometry", {}).get("coordinates", [None, None])
        name = (props.get("NAME") or "").strip()
        name_upper = name.upper()

        # Build address from GeoJSON fields
        block = str(props.get("ADDRESSBLOCKHOUSENUMBER") or "").strip()
        street = (props.get("ADDRESSSTREETNAME") or "").strip()
        postal = str(props.get("ADDRESSPOSTALCODE") or "").strip()
        addr_myenv = (props.get("ADDRESS_MYENV") or "").strip()
        address = addr_myenv or f"{block} {street}, Singapore {postal}".strip(", ")

        geo_lookup[name_upper] = {
            "name": name,
            "address": address,
            "longitude": coords[0] if coords else None,
            "latitude": coords[1] if coords else None,
            "photo_url": props.get("PHOTOURL"),
            "postal_code": postal,
            "street_name": street,
            "block_number": block,
            "status": props.get("STATUS"),
            "description": props.get("DESCRIPTION"),
            "num_cooked_stalls_geo": props.get("NUMBER_OF_COOKED_FOOD_STALLS"),
        }

    # ── Fallback: if CSV list is empty, build from GeoJSON alone ──
    if not hawker_list:
        logger.info("CSV list empty – building from GeoJSON alone (%d features)", len(geo_lookup))
        merged = []
        for geo in geo_lookup.values():
            merged.append({
                "name": geo["name"],
                "address": geo["address"],
                "type_of_centre": "HC",
                "owner": "Government",
                "no_of_stalls": _to_int(geo.get("num_cooked_stalls_geo")),
                "no_of_cooked_food_stalls": _to_int(geo.get("num_cooked_stalls_geo")),
                "no_of_mkt_produce_stalls": None,
                "latitude": geo["latitude"],
                "longitude": geo["longitude"],
                "photo_url": geo["photo_url"],
                "postal_code": geo["postal_code"],
                "status": geo["status"],
                "description": geo.get("description"),
            })
        return merged

    # ── Normal path: merge CSV with GeoJSON ──
    merged: list[dict] = []
    for row in hawker_list:
        name = (row.get("name_of_centre") or "").strip()
        name_upper = name.upper()

        # Try exact match first, then fuzzy
        geo = geo_lookup.get(name_upper)
        if not geo:
            for geo_name, geo_data in geo_lookup.items():
                if name_upper in geo_name or geo_name in name_upper:
                    geo = geo_data
                    break

        centre = {
            "name": name,
            "address": row.get("location_of_centre", "") or (geo["address"] if geo else ""),
            "type_of_centre": row.get("type_of_centre", ""),
            "owner": row.get("owner", ""),
            "no_of_stalls": _to_int(row.get("no_of_stalls")),
            "no_of_cooked_food_stalls": _to_int(row.get("no_of_cooked_food_stalls")),
            "no_of_mkt_produce_stalls": _to_int(row.get("no_of_mkt_produce_stalls")),
            "latitude": geo["latitude"] if geo else None,
            "longitude": geo["longitude"] if geo else None,
            "photo_url": geo["photo_url"] if geo else None,
            "postal_code": geo["postal_code"] if geo else None,
            "status": geo["status"] if geo else None,
            "description": geo.get("description") if geo else None,
        }
        merged.append(centre)

    logger.info("Merged %d hawker centres", len(merged))
    return merged


def _to_int(val) -> int | None:
    """Safely cast a value to int, returning None on failure."""
    if val is None:
        return None
    try:
        return int(val)
    except (ValueError, TypeError):
        return None
