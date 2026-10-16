"""
Application Configuration  (<<infrastructure>>)

All configs will be here
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Central settings object — all config accessed via settings.<FIELD>."""

    # TODO: Load all configs that are needed in the system or application
    pass


settings = Settings()
