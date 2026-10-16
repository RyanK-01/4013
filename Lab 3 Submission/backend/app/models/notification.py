"""
Notification Entity  (<<entity>>)

In-app notifications. user_id is set for targeted notifications
(e.g. "your stall was approved") and NULL for broadcast alerts
that are shown to all users.
"""

from sqlalchemy import String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Notification(Base):
    __tablename__ = "notifications"

    # TODO: define columns — id (pk), user_id (fk → users, nullable for broadcasts),
    #       title (str), message (text), notification_type (str, default "info"),
    #       is_read (default False), created_at
    pass
