"""
Report & Notification Schemas  (<<datatype>>)

Pydantic create/response models for bug reports, feature suggestions,
incorrect-info reports, crowd reports, notifications, and saved searches.
"""

from pydantic import BaseModel
from datetime import datetime


# ── Bug Reports ──

class BugReportCreate(BaseModel):
    """Bug report input — category and description."""
    # TODO: define category (str), description (str)
    pass


class BugReportOut(BaseModel):
    """Bug report response with status and timestamp."""
    # TODO: define id, user_id, category, description, status, created_at
    pass


# ── Feature Suggestions ──

class FeatureSuggestionCreate(BaseModel):
    """Feature suggestion input — just a description."""
    # TODO: define description (str)
    pass


class FeatureSuggestionOut(BaseModel):
    """Feature suggestion response with status and timestamp."""
    # TODO: define id, user_id, description, status, created_at
    pass


# ── Incorrect Info Reports ──

class IncorrectInfoReportCreate(BaseModel):
    """Incorrect info report — which stall, what's wrong, details."""
    # TODO: define stall_id (int), issue_type (str), description (str)
    pass


class IncorrectInfoReportOut(BaseModel):
    """Incorrect info report response with status and timestamp."""
    # TODO: define id, stall_id, user_id, issue_type, description, status, created_at
    pass


# ── Crowd Reports ──

class CrowdReportCreate(BaseModel):
    """Crowd level submission — stall_id and crowd percentage (0-100)."""
    # TODO: define stall_id (int), crowd_level (int)
    pass


class CrowdReportOut(BaseModel):
    """Crowd report response with approval status."""
    # TODO: define id, stall_id, user_id, crowd_level, is_approved, created_at
    pass


# ── Notifications ──

class NotificationOut(BaseModel):
    """Notification response — user_id is None for broadcasts."""
    # TODO: define id, user_id, title, message, notification_type, is_read, created_at
    pass


# ── Saved Searches ──

class SavedSearchCreate(BaseModel):
    """Save a named filter config for quick reuse."""
    # TODO: define name (str), filters (dict)
    pass


class SavedSearchOut(BaseModel):
    """Saved search response with filter data and timestamp."""
    # TODO: define id, user_id, name, filters, created_at
    pass
