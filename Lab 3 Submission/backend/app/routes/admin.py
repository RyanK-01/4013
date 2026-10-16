"""
Admin Routes  (<<boundary>>)

Admin-only endpoints (all require JWT + admin role) for:
  - Dashboard statistics
  - Stall CRUD and approval/rejection of user submissions
  - Review and crowd report moderation
  - Bug report / feature suggestion / incorrect-info management
  - User account management (list, deactivate)
  - Cuisine type management
basically all adminn features
"""

from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database import get_db
from app.models.user import User
from app.models.stall import Stall, StallDietaryTag, MenuItem, CuisineType
from app.models.review import Review
from app.models.crowd_report import CrowdReport
from app.models.report import BugReport, FeatureSuggestion, IncorrectInfoReport
from app.models.notification import Notification
from app.schemas.stall import StallOut, StallCreate, StallUpdate
from app.middleware.auth import require_admin

router = APIRouter(prefix="/api/admin", tags=["admin"])


class ApprovalDecision(BaseModel):
    """Admin's approve/reject decision with optional reason."""
    # TODO: define approved (bool), reason (str|None)
    pass


class BroadcastNotification(BaseModel):
    """Payload for sending a broadcast notification to all users."""
    # TODO: define title (str), message (str), notification_type (str, default "alert")
    pass


# ── Dashboard ──

@router.get("/stats")
def get_admin_stats(db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    """Return aggregate counts for the admin dashboard (stalls, reviews, reports, users)."""
    # TODO: count total/pending stalls, pending reviews, pending crowd reports,
    #       total users, pending bug reports, feature suggestions, incorrect info reports
    pass


# ── Stall Management ──

@router.get("/stalls")
def admin_list_stalls(approved: bool | None = None, db: Session = Depends(get_db),
                      admin: User = Depends(require_admin)):
    """List all stalls, optionally filtered by approval status."""
    # TODO: query stalls with optional approved filter, order by created_at desc
    pass


@router.post("/stalls", response_model=StallOut)
def admin_create_stall(data: StallCreate, db: Session = Depends(get_db),
                       admin: User = Depends(require_admin)):
    """Create a new stall (auto-approved since created by admin)."""
    # TODO: create Stall with is_approved=True, add dietary tags + menu items
    pass


@router.put("/stalls/{stall_id}")
def admin_update_stall(stall_id: int, data: StallUpdate, db: Session = Depends(get_db),
                       admin: User = Depends(require_admin)):
    """Update stall fields. Replaces dietary tags if provided."""
    # TODO: find stall or 404, apply changed fields, replace tags if included
    pass


@router.delete("/stalls/{stall_id}")
def admin_delete_stall(stall_id: int, db: Session = Depends(get_db),
                       admin: User = Depends(require_admin)):
    """Permanently delete a stall."""
    # TODO: find stall or 404, delete from DB
    pass


# ── Approve / Reject Submissions ──

@router.put("/stalls/{stall_id}/approve")
def approve_reject_stall(stall_id: int, decision: ApprovalDecision,
                         db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    """Approve or reject a user-submitted stall, notify the submitter."""
    # TODO: set is_approved, store rejection_reason, create Notification for submitter
    pass


@router.get("/reviews")
def admin_list_reviews(approved: bool | None = None, db: Session = Depends(get_db),
                       admin: User = Depends(require_admin)):
    """List all reviews, optionally filtered by approval status."""
    # TODO: query reviews with stall_name and username, optional approved filter
    pass


@router.put("/reviews/{review_id}/approve")
def approve_reject_review(review_id: int, decision: ApprovalDecision,
                          db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    """Approve or reject a review, notify the author."""
    # TODO: set is_approved, store rejection_reason, create Notification for author
    pass


@router.get("/crowd-reports")
def admin_list_crowd_reports(approved: bool | None = None, db: Session = Depends(get_db),
                             admin: User = Depends(require_admin)):
    """List all crowd reports, optionally filtered by approval status."""
    # TODO: query crowd reports with stall_name and username
    pass


@router.put("/crowd-reports/{report_id}/approve")
def approve_reject_crowd_report(report_id: int, decision: ApprovalDecision,
                                db: Session = Depends(get_db),
                                admin: User = Depends(require_admin)):
    """Approve/reject a crowd report. On approval, update the stall's crowd_level."""
    # TODO: set is_approved, update stall.crowd_level if approved, notify reporter
    pass


# ── User Reports & Feedback ──

@router.get("/bug-reports")
def admin_list_bug_reports(db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    """List all bug reports, newest first."""
    # TODO: query BugReport with username, order by created_at desc
    pass


@router.put("/bug-reports/{report_id}/status")
def update_bug_report_status(report_id: int, status: str = Body(..., embed=True),
                             db: Session = Depends(get_db),
                             admin: User = Depends(require_admin)):
    """Update a bug report's status (e.g. pending → reviewed → resolved)."""
    # TODO: find report or 404, update status field
    pass


@router.get("/feature-suggestions")
def admin_list_feature_suggestions(db: Session = Depends(get_db),
                                   admin: User = Depends(require_admin)):
    """List all feature suggestions, newest first."""
    # TODO: query FeatureSuggestion with username, order by created_at desc
    pass


@router.get("/incorrect-info-reports")
def admin_list_incorrect_info_reports(db: Session = Depends(get_db),
                                     admin: User = Depends(require_admin)):
    """List all incorrect-info reports, newest first."""
    # TODO: query IncorrectInfoReport with username, order by created_at desc
    pass


@router.put("/incorrect-info-reports/{report_id}/status")
def update_incorrect_info_status(report_id: int, status: str = Body(..., embed=True),
                                 db: Session = Depends(get_db),
                                 admin: User = Depends(require_admin)):
    """Update an incorrect-info report's status."""
    # TODO: find report or 404, update status field
    pass


# ── Notifications ──

@router.post("/notifications/broadcast")
def broadcast_notification(data: BroadcastNotification, db: Session = Depends(get_db),
                           admin: User = Depends(require_admin)):
    """Send a broadcast notification visible to all users (user_id = None)."""
    # TODO: create Notification with user_id=None, save to DB
    pass


# ── User Management ──

@router.get("/users")
def admin_list_users(db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    """List all registered users, newest first."""
    # TODO: query all users, order by created_at desc
    pass


@router.put("/users/{user_id}/deactivate")
def deactivate_user(user_id: int, db: Session = Depends(get_db),
                    admin: User = Depends(require_admin)):
    """Deactivate (soft-delete) a user account by setting is_active = False."""
    # TODO: find user or 404, set is_active = False
    pass


# ── Cuisine Types ──

@router.get("/cuisine-types")
def admin_list_cuisine_types(db: Session = Depends(get_db),
                             admin: User = Depends(require_admin)):
    """List all cuisine types alphabetically."""
    # TODO: query CuisineType ordered by name
    pass


@router.post("/cuisine-types")
def admin_add_cuisine_type(name: str = Body(..., embed=True), db: Session = Depends(get_db),
                           admin: User = Depends(require_admin)):
    """Add a new cuisine type to the system."""
    # TODO: create CuisineType with given name, save to DB
    pass


@router.delete("/cuisine-types/{cuisine_id}")
def admin_delete_cuisine_type(cuisine_id: int, db: Session = Depends(get_db),
                              admin: User = Depends(require_admin)):
    """Delete a cuisine type by ID."""
    # TODO: find cuisine type or 404, delete from DB
    pass


# ── Gov Data Sync ──

@router.post("/sync-gov-data")
async def sync_gov_data(db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    """Re-fetch hawker centre data from data.gov.sg and insert any new centres."""
    # TODO: call fetch_hawker_list + fetch_hawker_geojson, merge, insert new (skip existing by name)
    pass
