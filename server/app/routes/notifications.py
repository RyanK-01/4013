"""API routes for user notification retrieval and read-status management."""

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
def get_notifications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """List the user's notifications plus broadcasts, newest first (max 50). Requires JWT."""
    notifications = (
        db.query(Notification)
        .filter(
            or_(
                Notification.user_id == current_user.id,
                Notification.user_id.is_(None),  # Broadcast notifications
            )
        )
        .order_by(Notification.created_at.desc())
        .limit(50)
        .all()
    )
    return notifications


@router.put("/{notification_id}/read")
def mark_as_read(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Mark a single notification as read. Requires JWT."""
    notif = (
        db.query(Notification)
        .filter(Notification.id == notification_id)
        .filter(
            or_(
                Notification.user_id == current_user.id,
                Notification.user_id.is_(None),
            )
        )
        .first()
    )
    if not notif:
        raise HTTPException(status_code=404, detail="Notification not found")
    notif.is_read = True
    db.commit()
    return {"status": "read"}


@router.put("/read-all")
def mark_all_as_read(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Mark all of the current user's unread notifications as read. Requires JWT."""
    db.query(Notification).filter(
        Notification.user_id == current_user.id,
        Notification.is_read == False,
    ).update({"is_read": True})
    db.commit()
    return {"status": "all read"}


@router.get("/unread-count")
def get_unread_count(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Return the count of unread notifications (user-specific + broadcasts). Requires JWT."""
    count = (
        db.query(Notification)
        .filter(
            or_(
                Notification.user_id == current_user.id,
                Notification.user_id.is_(None),
            ),
            Notification.is_read == False,
        )
        .count()
    )
    return {"count": count}
