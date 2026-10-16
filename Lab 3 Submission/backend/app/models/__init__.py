"""
Entity Layer — ORM Model Registry  (<<entity>>)

Re-exports every SQLAlchemy model so that a wildcard import registers them
all with the declarative Base.
"""

from app.models.user import User
from app.models.stall import Stall, MenuItem, StallDietaryTag, CuisineType
from app.models.review import Review
from app.models.favourite import Favourite
from app.models.crowd_report import CrowdReport
from app.models.report import BugReport, FeatureSuggestion, IncorrectInfoReport
from app.models.notification import Notification
from app.models.saved_search import SavedSearch

# To import all models
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
