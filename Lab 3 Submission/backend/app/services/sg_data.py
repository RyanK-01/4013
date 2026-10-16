"""
Singapore Government Data Integration  (<<control>>)

Fetches hawker centre data from two NEA datasets on data.gov.sg:
  1. Hawker List CSV — centre names, addresses, stall counts, ownership
  2. Hawker GeoJSON — GPS coordinates, photos, statuses
Then merges them by centre name for database seeding.
"""

import httpx
import logging
from typing import Any

logger = logging.getLogger(__name__)

# Resource id for data sets
HAWKER_LIST_RESOURCE = "d_68a42f09f350881996d83f9cd73ab02f"
HAWKER_GEOJSON_DATASET = "d_4a086da0a5553be1d89383cd90d07ecd"

DATAGOVSG_SEARCH_URL = "https://data.gov.sg/api/action/datastore_search"
DATAGOVSG_POLL_URL = (
    "https://api-open.data.gov.sg/v1/public/api/datasets/{dataset_id}/poll-download"
)


async def fetch_hawker_list() -> list[dict[str, Any]]:

"""Fetch all hawker centres (e.g. name, address from the data.gov.sg CSV dataset (paginated).

This function fetches the hawker centre listing, handling pagination
    where required, and returns the dataset as a list of dictionaries
    for further processing.

    Returns:
        A list of hawker centre records from the CSV dataset.

    Notes:
        Used during data import or database seeding to obtain the base
        hawker centre information. 
        """

    # TODO: get data from data.gov.sg and return as list of dicts
    pass


async def fetch_hawker_geojson() -> dict[str, Any]:
    """Fetch Hawker Centres GeoJSON (e.g. coordinates, geometry) via data.gov.sg poll-download → S3 signed URL.
     Returns:
        A dictionary containing the GeoJSON data.

    Notes:
        Used during data import or database seeding to obtain location
        and geometry data for hawker centres.
        """
    # TODO: get signed URL from poll endpoint, then download actual GeoJSON
    pass


def merge_hawker_data(
    hawker_list: list[dict], geojson: dict
) -> list[dict[str, Any]]:
   """
    Combine hawker centre records from the CSV and GeoJSON datasets above.

    This function matches hawker centres across both sources, typically
    by centre name, and produces a combined dataset suitable for database
    insertion.

    Args:
        hawker_list: Hawker centre records from the CSV dataset.
        geojson: Geographic hawker centre data from the GeoJSON dataset.

    Returns:
        A merged list of hawker centre records containing both descriptive
        and geographic information.

    Notes:
        Used by the database seeding process to prepare consolidated
        hawker centre data before insertion into DB.
        
    """
    # TODO: build geo lookup by name, match with CSV
    pass
