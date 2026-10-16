"""Re-exports all ORM models so that ``from app.models import *`` registers them with SQLAlchemy."""

from app.models.user import User
from app.models.stall import Stall, MenuItem, StallDietaryTag, CuisineType
from app.models.review import Review
from app.models.favourite import Favourite
from app.models.crowd_report import CrowdReport
from app.models.report import BugReport, FeatureSuggestion, IncorrectInfoReport
from app.models.notification import Notification
from app.models.saved_search import SavedSearch

__all__ = [
    "User",
    "Stall", "MenuItem", "StallDietaryTag", "CuisineType",
    "Review",
    "Favourite",
    "CrowdReport",
    "BugReport", "FeatureSuggestion", "IncorrectInfoReport",
    "Notification",
    "SavedSearch",
]
