"""Application configuration loaded from environment variables with sensible defaults."""

import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Centralised settings for database, JWT auth, file uploads, and external API credentials."""
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/sc2006_hawker")

    # JWT Auth
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))

    # File uploads
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "uploads")

    # OneMap API https://www.onemap.gov.sg/apidocs/register
    ONEMAP_EMAIL: str = os.getenv("ONEMAP_EMAIL", "")
    ONEMAP_PASSWORD: str = os.getenv("ONEMAP_PASSWORD", "")

    # data.gov.sg
    DATAGOVSG_HAWKER_LIST_RESOURCE: str = "d_68a42f09f350881996d83f9cd73ab02f"
    DATAGOVSG_HAWKER_GEOJSON_DATASET: str = "d_4a086da0a5553be1d89383cd90d07ecd"


settings = Settings()
