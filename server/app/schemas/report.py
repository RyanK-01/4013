"""Pydantic schemas for bug reports, feature suggestions, incorrect-info reports, crowd reports, notifications, and saved searches."""

from pydantic import BaseModel
from datetime import datetime


class BugReportCreate(BaseModel):
    """Request body for filing a bug report."""
    category: str
    description: str


class BugReportOut(BaseModel):
    """Bug report data returned in API responses."""
    id: int
    user_id: int
    category: str
    description: str
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}


class FeatureSuggestionCreate(BaseModel):
    """Request body for submitting a feature suggestion."""
    description: str


class FeatureSuggestionOut(BaseModel):
    """Feature suggestion data returned in API responses."""
    id: int
    user_id: int
    description: str
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}


class IncorrectInfoReportCreate(BaseModel):
    """Request body for reporting incorrect stall information."""
    stall_id: int
    issue_type: str
    description: str


class IncorrectInfoReportOut(BaseModel):
    """Incorrect-info report data returned in API responses."""
    id: int
    stall_id: int
    user_id: int
    issue_type: str
    description: str
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}


class CrowdReportCreate(BaseModel):
    """Request body for submitting a crowd-level observation."""
    stall_id: int
    crowd_level: int  # 0-100


class CrowdReportOut(BaseModel):
    """Crowd report data returned in API responses."""
    id: int
    stall_id: int
    user_id: int
    crowd_level: int
    is_approved: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class NotificationOut(BaseModel):
    """Notification data returned in API responses."""
    id: int
    user_id: int | None
    title: str
    message: str
    notification_type: str
    is_read: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class SavedSearchCreate(BaseModel):
    """Request body for saving a named search filter configuration."""
    name: str
    filters: dict


class SavedSearchOut(BaseModel):
    """Saved search data returned in API responses."""
    id: int
    user_id: int
    name: str
    filters: dict
    created_at: datetime

    model_config = {"from_attributes": True}
