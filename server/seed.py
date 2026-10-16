"""
Seed script – Populates the database with:
  1. Admin + test user accounts
  2. Default cuisine types
  3. Hawker centre data from data.gov.sg (NEA)
     - List of Government Markets & Hawker Centres (107 centres)
     - Hawker Centres GeoJSON (coordinates & photos)

Run:  python seed.py
"""

import asyncio
import sys
from app.database import SessionLocal, engine, Base
from app.models.user import User
from app.models.stall import Stall, MenuItem, StallDietaryTag, CuisineType
from app.middleware.auth import hash_password
from app.services.sg_data import fetch_hawker_list, fetch_hawker_geojson, merge_hawker_data

# Create all tables
Base.metadata.create_all(bind=engine)
db = SessionLocal()


def seed_users():
    """Create admin and test user accounts."""
    if not db.query(User).filter(User.email == "admin@hawker.sg").first():
        db.add(User(
            email="admin@hawker.sg",
            username="admin",
            password_hash=hash_password("admin123"),
            role="admin",
        ))
        print("[+] Created admin: admin@hawker.sg / admin123")

    if not db.query(User).filter(User.email == "user@test.com").first():
        db.add(User(
            email="user@test.com",
            username="testuser",
            password_hash=hash_password("user123"),
            role="user",
        ))
        print("[+] Created test user: user@test.com / user123")

    db.commit()


def seed_cuisine_types():
    """Insert default cuisine categories."""
    defaults = [
        "Chinese Cuisine", "Malay Cuisine", "Indian Cuisine", "Western",
        "Seafood", "Japanese", "Korean", "Thai", "Halal", "Vegetarian",
        "Desserts", "Drinks", "Mixed / Others",
    ]
    for name in defaults:
        if not db.query(CuisineType).filter(CuisineType.name == name).first():
            db.add(CuisineType(name=name))
    db.commit()
    print(f"[+] Cuisine types seeded ({len(defaults)})")


async def seed_hawker_centres():
    """
    Fetch hawker centre data from data.gov.sg and populate the stalls table.
    Merges the CSV list (names, addresses, stall counts) with the GeoJSON
    (coordinates, photos) to produce enriched records.
    """
    print("[*] Fetching hawker data from data.gov.sg ...")

    try:
        hawker_list = await fetch_hawker_list()
        print(f"    - Hawker list: {len(hawker_list)} centres")
    except Exception as e:
        print(f"[!] Failed to fetch hawker list: {e}")
        hawker_list = []

    try:
        geojson = await fetch_hawker_geojson()
        feature_count = len(geojson.get("features", []))
        print(f"    - GeoJSON: {feature_count} features")
    except Exception as e:
        print(f"[!] Failed to fetch GeoJSON: {e}")
        geojson = {"features": []}

    if not hawker_list and not geojson.get("features"):
        print("[!] No hawker data retrieved – skipping stall seeding")
        return

    if not hawker_list:
        print("[*] CSV list unavailable – using GeoJSON as primary source")

    merged = merge_hawker_data(hawker_list, geojson)
    created = 0

    for centre in merged:
        # Skip if already exists (by name)
        if db.query(Stall).filter(Stall.name == centre["name"]).first():
            continue

        # Determine type label
        type_map = {"HC": "Hawker Centre", "MK": "Market", "MHC": "Market & Hawker Centre"}
        centre_type = type_map.get(centre["type_of_centre"], "Hawker Centre")

        stall = Stall(
            name=centre["name"],
            description=f'{centre_type} with {centre.get("no_of_cooked_food_stalls") or "?"} cooked food stalls. Data from NEA / data.gov.sg.',
            address=centre["address"],
            latitude=centre["latitude"],
            longitude=centre["longitude"],
            cuisine_type="Mixed / Others",  # Hawker centres serve multiple cuisines
            price_range_min=3.00,  # Typical SG hawker price range
            price_range_max=8.00,
            indoor_outdoor="Indoor" if "indoor" in centre["name"].lower() else None,
            image_url=centre.get("photo_url"),
            is_approved=True,  # Government data is pre-approved
        )
        db.add(stall)
        created += 1

    db.commit()
    print(f"[+] Seeded {created} hawker centres from data.gov.sg")


def seed_sample_stalls():
    """
    Add a handful of popular individual food stalls (not in gov data)
    so the recommendation engine has variety to work with.
    """
    sample_stalls = [
        {
            "name": "Tian Tian Hainanese Chicken Rice",
            "description": "Famous chicken rice stall at Maxwell Food Centre. Michelin Bib Gourmand.",
            "address": "1 Kadayanallur St, #01-10/11, Maxwell Food Centre, Singapore 069184",
            "latitude": 1.2805, "longitude": 103.8448,
            "cuisine_type": "Chinese Cuisine",
            "price_range_min": 3.50, "price_range_max": 6.00,
            "operating_hours": {"mon": "10:00-19:30", "tue": "10:00-19:30", "wed": "Closed", "thu": "10:00-19:30", "fri": "10:00-19:30", "sat": "10:00-19:30", "sun": "10:00-19:30"},
            "indoor_outdoor": "Indoor",
            "google_rating": 4.3, "google_review_count": 12500,
            "tags": [], "menu": [
                {"name": "Chicken Rice", "price": 5.00, "description": "Signature Hainanese chicken rice"},
                {"name": "Roasted Chicken Rice", "price": 5.50, "description": "Roasted version"},
            ],
        },
        {
            "name": "Allauddin's Briyani",
            "description": "Famous briyani at Tekka Centre – authentic Indian-Muslim cuisine.",
            "address": "2 Tekka Pl, #01-222, Tekka Centre, Singapore 540002",
            "latitude": 1.3066, "longitude": 103.8498,
            "cuisine_type": "Indian Cuisine",
            "price_range_min": 5.00, "price_range_max": 8.00,
            "operating_hours": {"mon": "07:00-21:00", "tue": "07:00-21:00", "wed": "07:00-21:00", "thu": "07:00-21:00", "fri": "07:00-21:00", "sat": "07:00-21:00", "sun": "07:00-21:00"},
            "indoor_outdoor": "Indoor",
            "google_rating": 4.2, "google_review_count": 5400,
            "tags": ["Halal"], "menu": [
                {"name": "Chicken Briyani", "price": 6.00, "description": "Fragrant chicken briyani"},
                {"name": "Mutton Briyani", "price": 7.50, "description": "Tender mutton briyani"},
            ],
        },
        {
            "name": "Liao Fan Hawker Chan",
            "description": "Cheapest Michelin-starred meal in the world – soya sauce chicken rice.",
            "address": "78 Smith St, #02-126, Chinatown Complex, Singapore 058972",
            "latitude": 1.2823, "longitude": 103.8431,
            "cuisine_type": "Chinese Cuisine",
            "price_range_min": 3.00, "price_range_max": 7.00,
            "operating_hours": {"mon": "10:30-20:00", "tue": "10:30-20:00", "wed": "Closed", "thu": "10:30-20:00", "fri": "10:30-20:00", "sat": "10:30-20:00", "sun": "10:30-20:00"},
            "indoor_outdoor": "Indoor",
            "google_rating": 4.1, "google_review_count": 15000,
            "tags": [], "menu": [
                {"name": "Soya Sauce Chicken Rice", "price": 3.80, "description": "Michelin-starred chicken rice"},
                {"name": "Char Siew Rice", "price": 5.00, "description": "BBQ pork rice"},
            ],
        },
        {
            "name": "Nasi Lemak Ayam Taliwang",
            "description": "Authentic Malay nasi lemak at Old Airport Road Food Centre.",
            "address": "51 Old Airport Rd, #01-68, Old Airport Road Food Centre, Singapore 390051",
            "latitude": 1.3134, "longitude": 103.8827,
            "cuisine_type": "Malay Cuisine",
            "price_range_min": 3.00, "price_range_max": 6.00,
            "operating_hours": {"mon": "06:30-14:00", "tue": "06:30-14:00", "wed": "06:30-14:00", "thu": "06:30-14:00", "fri": "06:30-14:00", "sat": "06:30-14:00", "sun": "Closed"},
            "indoor_outdoor": "Indoor",
            "google_rating": 4.1, "google_review_count": 3200,
            "tags": ["Halal"], "menu": [
                {"name": "Nasi Lemak", "price": 3.50, "description": "Classic nasi lemak"},
                {"name": "Nasi Lemak Ayam", "price": 5.50, "description": "With fried chicken"},
            ],
        },
        {
            "name": "Komala Vilas",
            "description": "Iconic South Indian vegetarian restaurant since 1947.",
            "address": "76-78 Serangoon Rd, Singapore 217981",
            "latitude": 1.3074, "longitude": 103.8521,
            "cuisine_type": "Indian Cuisine",
            "price_range_min": 3.00, "price_range_max": 10.00,
            "operating_hours": {"mon": "07:00-22:00", "tue": "07:00-22:00", "wed": "07:00-22:00", "thu": "07:00-22:00", "fri": "07:00-22:00", "sat": "07:00-22:00", "sun": "07:00-22:00"},
            "indoor_outdoor": "Indoor",
            "google_rating": 4.2, "google_review_count": 6200,
            "tags": ["Vegetarian", "Halal"], "menu": [
                {"name": "Thali Set", "price": 7.50, "description": "South Indian thali meal"},
                {"name": "Masala Dosa", "price": 4.50, "description": "Crispy dosa with potato filling"},
            ],
        },
        {
            "name": "Outram Park Fried Kway Teow",
            "description": "Legendary char kway teow at Hong Lim Food Centre.",
            "address": "531A Upper Cross St, #02-17, Hong Lim Food Centre, Singapore 051531",
            "latitude": 1.2855, "longitude": 103.8456,
            "cuisine_type": "Chinese Cuisine",
            "price_range_min": 4.00, "price_range_max": 6.00,
            "operating_hours": {"mon": "06:00-16:30", "tue": "06:00-16:30", "wed": "06:00-16:30", "thu": "06:00-16:30", "fri": "06:00-16:30", "sat": "Closed", "sun": "Closed"},
            "indoor_outdoor": "Indoor",
            "google_rating": 4.0, "google_review_count": 2100,
            "tags": ["Seafood"], "menu": [
                {"name": "Fried Kway Teow", "price": 5.00, "description": "Wok-fried flat rice noodles with cockles"},
            ],
        },
    ]

    created = 0
    for s in sample_stalls:
        if db.query(Stall).filter(Stall.name == s["name"]).first():
            continue
        stall = Stall(
            name=s["name"], description=s["description"], address=s["address"],
            latitude=s["latitude"], longitude=s["longitude"],
            cuisine_type=s["cuisine_type"],
            price_range_min=s["price_range_min"], price_range_max=s["price_range_max"],
            operating_hours=s.get("operating_hours"),
            indoor_outdoor=s.get("indoor_outdoor"),
            google_rating=s.get("google_rating"),
            google_review_count=s.get("google_review_count"),
            is_approved=True,
        )
        db.add(stall)
        db.flush()

        for tag in s.get("tags", []):
            db.add(StallDietaryTag(stall_id=stall.id, tag=tag))
        for item in s.get("menu", []):
            db.add(MenuItem(stall_id=stall.id, name=item["name"], price=item["price"], description=item.get("description")))

        created += 1

    db.commit()
    print(f"[+] Seeded {created} sample food stalls")


async def main():
    print("=" * 50)
    print("SC2006 HawkerLah! – Database Seeder")
    print("=" * 50)

    seed_users()
    seed_cuisine_types()
    await seed_hawker_centres()
    seed_sample_stalls()

    total = db.query(Stall).count()
    approved = db.query(Stall).filter(Stall.is_approved == True).count()
    print(f"\n{'=' * 50}")
    print(f"Seed complete! {total} stalls total ({approved} approved)")
    print(f"{'=' * 50}")

    db.close()


if __name__ == "__main__":
    asyncio.run(main())
