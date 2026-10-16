"""
Notification Routes  (<<boundary>>)

Manages in-app notifications for the user,
marking individual or all as read, and retrieving unread count for the badge.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.database import get_db
from app.models.user import User
from app.models.notification import Notification
from app.schemas.report import NotificationOut
from app.middleware.auth import get_current_user

router = APIRouter(prefix="/api/notifications", tags=["notifications"])


@router.get("/", response_model=list[NotificationOut])
def get_notifications(db: Session = Depends(get_db),
                      current_user: User = Depends(get_current_user)):
    """List user's notifications plus broadcast notifications (user_id IS NULL), max 50."""
    # TODO: query where user_id = current user OR user_id is None, order newest first
    pass


@router.put("/{notification_id}/read")
def mark_as_read(notification_id: int, db: Session = Depends(get_db),
                 current_user: User = Depends(get_current_user)):
    """Mark a single notification as read."""
    # TODO: find notification (check ownership or broadcast), set is_read = True
    pass


@router.put("/read-all")
def mark_all_as_read(db: Session = Depends(get_db),
                     current_user: User = Depends(get_current_user)):
    """Mark all of the current user's unread notifications as read."""
    # TODO: bulk update is_read = True for user's unread notifications
    pass


@router.get("/unread-count")
def get_unread_count(db: Session = Depends(get_db),
                     current_user: User = Depends(get_current_user)):
    """Return the count of unread notifications (for the header badge)."""
    # TODO: count where (user_id = current user OR user_id is None) AND is_read = False
    pass
