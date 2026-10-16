"""Admin-only API routes for dashboard stats, content moderation, and system management."""

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


# ── Dashboard Stats ──

@router.get("/stats")
def get_admin_stats(
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    """Return aggregate counts for the admin dashboard (stalls, reviews, reports, users). Requires admin role."""
    return {
        "total_stalls": db.query(Stall).filter(Stall.is_approved == True).count(),
        "pending_stalls": db.query(Stall).filter(Stall.is_approved == False).count(),
        "pending_reviews": db.query(Review).filter(Review.is_approved == False).count(),
        "pending_crowd_reports": db.query(CrowdReport).filter(CrowdReport.is_approved == False).count(),
        "total_users": db.query(User).filter(User.role == "user").count(),
        "bug_reports_pending": db.query(BugReport).filter(BugReport.status == "pending").count(),
        "feature_suggestions": db.query(FeatureSuggestion).filter(FeatureSuggestion.status == "pending").count(),
        "incorrect_info_reports": db.query(IncorrectInfoReport).filter(IncorrectInfoReport.status == "pending").count(),
    }


# ── Stall Management ──

@router.get("/stalls")
def admin_list_stalls(
    approved: bool | None = None,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    """List all stalls, optionally filtered by approval status. Requires admin role."""
    query = db.query(Stall)
    if approved is not None:
        query = query.filter(Stall.is_approved == approved)
    return query.order_by(Stall.created_at.desc()).all()


@router.post("/stalls", response_model=StallOut)
def admin_create_stall(
    data: StallCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    """Create a new stall (auto-approved). Requires admin role."""
    stall = Stall(
        name=data.name,
        description=data.description,
        address=data.address,
        latitude=data.latitude,
        longitude=data.longitude,
        cuisine_type=data.cuisine_type,
        price_range_min=data.price_range_min,
        price_range_max=data.price_range_max,
        operating_hours=data.operating_hours,
        indoor_outdoor=data.indoor_outdoor,
        is_approved=True,  # Admin-created stalls are auto-approved
    )
    db.add(stall)
    db.flush()

    for tag_name in data.dietary_tags:
        db.add(StallDietaryTag(stall_id=stall.id, tag=tag_name))
    for item in data.menu_items:
        db.add(MenuItem(stall_id=stall.id, name=item.name, price=item.price, description=item.description))

    db.commit()
    db.refresh(stall)
    return stall


@router.put("/stalls/{stall_id}")
def admin_update_stall(
    stall_id: int,
    data: StallUpdate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    """Update stall fields (including dietary tags replacement). Requires admin role."""
    stall = db.query(Stall).filter(Stall.id == stall_id).first()
    if not stall:
        raise HTTPException(status_code=404, detail="Stall not found")

    for field, value in data.model_dump(exclude_unset=True).items():
        if field == "dietary_tags":
            # Replace tags
            db.query(StallDietaryTag).filter(StallDietaryTag.stall_id == stall_id).delete()
            for tag_name in value:
                db.add(StallDietaryTag(stall_id=stall_id, tag=tag_name))
        else:
            setattr(stall, field, value)

    db.commit()
    db.refresh(stall)
    return stall


@router.delete("/stalls/{stall_id}")
def admin_delete_stall(
    stall_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    """Permanently delete a stall by ID. Requires admin role."""
    stall = db.query(Stall).filter(Stall.id == stall_id).first()
    if not stall:
        raise HTTPException(status_code=404, detail="Stall not found")
    db.delete(stall)
    db.commit()
    return {"status": "deleted"}


# ── Approve / Reject Stall Submissions ──

class ApprovalDecision(BaseModel):
    approved: bool
    reason: str | None = None


@router.put("/stalls/{stall_id}/approve")
def approve_reject_stall(
    stall_id: int,
    decision: ApprovalDecision,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    """Approve or reject a user-submitted stall. Notifies the submitter. Requires admin role."""
    stall = db.query(Stall).filter(Stall.id == stall_id).first()
    if not stall:
        raise HTTPException(status_code=404, detail="Stall not found")

    stall.is_approved = decision.approved
    if not decision.approved:
        stall.rejection_reason = decision.reason

    # Notify user
    if stall.submitted_by:
        status_text = "approved" if decision.approved else "rejected"
        notif = Notification(
            user_id=stall.submitted_by,
            title=f"Stall Submission {status_text.title()}",
            message=f"Your stall submission '{stall.name}' has been {status_text}."
            + (f" Reason: {decision.reason}" if decision.reason else ""),
            notification_type="approval" if decision.approved else "rejection",
        )
        db.add(notif)

    db.commit()
    return {"status": "approved" if decision.approved else "rejected"}


# ── Approve / Reject Reviews ──

@router.get("/reviews")
def admin_list_reviews(
    approved: bool | None = None,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    """List all reviews with optional approval filter. Requires admin role."""
    query = db.query(Review)
    if approved is not None:
        query = query.filter(Review.is_approved == approved)
    reviews = query.order_by(Review.created_at.desc()).all()
    result = []
    for r in reviews:
        result.append({
            "id": r.id,
            "stall_id": r.stall_id,
            "stall_name": r.stall.name if r.stall else None,
            "user_id": r.user_id,
            "username": r.user.username if r.user else None,
            "rating": r.rating,
            "comment": r.comment,
            "photo_url": r.photo_url,
            "is_approved": r.is_approved,
            "created_at": r.created_at,
        })
    return result


@router.put("/reviews/{review_id}/approve")
def approve_reject_review(
    review_id: int,
    decision: ApprovalDecision,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    """Approve or reject a review. Notifies the author. Requires admin role."""
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    review.is_approved = decision.approved
    if not decision.approved:
        review.rejection_reason = decision.reason

    notif = Notification(
        user_id=review.user_id,
        title="Review " + ("Approved" if decision.approved else "Rejected"),
        message=f"Your review has been {'approved and is now visible' if decision.approved else 'rejected'}."
        + (f" Reason: {decision.reason}" if decision.reason else ""),
        notification_type="approval" if decision.approved else "rejection",
    )
    db.add(notif)
    db.commit()
    return {"status": "approved" if decision.approved else "rejected"}


# ── Approve / Reject Crowd Reports ──

@router.get("/crowd-reports")
def admin_list_crowd_reports(
    approved: bool | None = None,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    """List all crowd-level reports with optional approval filter. Requires admin role."""
    query = db.query(CrowdReport)
    if approved is not None:
        query = query.filter(CrowdReport.is_approved == approved)
    reports = query.order_by(CrowdReport.created_at.desc()).all()
    result = []
    for r in reports:
        result.append({
            "id": r.id,
            "stall_id": r.stall_id,
            "stall_name": r.stall.name if r.stall else None,
            "user_id": r.user_id,
            "username": r.user.username if r.user else None,
            "crowd_level": r.crowd_level,
            "is_approved": r.is_approved,
            "created_at": r.created_at,
        })
    return result


@router.put("/crowd-reports/{report_id}/approve")
def approve_reject_crowd_report(
    report_id: int,
    decision: ApprovalDecision,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    """Approve or reject a crowd report. Updates stall crowd_level on approval. Requires admin role."""
    report = db.query(CrowdReport).filter(CrowdReport.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Crowd report not found")

    report.is_approved = decision.approved
    if not decision.approved:
        report.rejection_reason = decision.reason

    # Update stall crowd level if approved
    if decision.approved:
        stall = db.query(Stall).filter(Stall.id == report.stall_id).first()
        if stall:
            stall.crowd_level = report.crowd_level

    notif = Notification(
        user_id=report.user_id,
        title="Crowd Report " + ("Approved" if decision.approved else "Rejected"),
        message=f"Your crowd level report has been {'approved' if decision.approved else 'rejected'}."
        + (f" Reason: {decision.reason}" if decision.reason else ""),
        notification_type="approval" if decision.approved else "rejection",
    )
    db.add(notif)
    db.commit()
    return {"status": "approved" if decision.approved else "rejected"}


# ── User Reports & Feedback ──

@router.get("/bug-reports")
def admin_list_bug_reports(
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    """List all user-submitted bug reports, newest first. Requires admin role."""
    reports = db.query(BugReport).order_by(BugReport.created_at.desc()).all()
    return [{
        "id": r.id,
        "user_id": r.user_id,
        "username": r.user.username if r.user else None,
        "category": r.category,
        "description": r.description,
        "status": r.status,
        "created_at": r.created_at,
    } for r in reports]


@router.put("/bug-reports/{report_id}/status")
def update_bug_report_status(
    report_id: int,
    status: str = Body(..., embed=True),
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    """Update the status of a bug report (e.g. pending, resolved). Requires admin role."""
    report = db.query(BugReport).filter(BugReport.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Bug report not found")
    report.status = status
    db.commit()
    return {"status": status}


@router.get("/feature-suggestions")
def admin_list_feature_suggestions(
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    """List all feature suggestions, newest first. Requires admin role."""
    suggestions = db.query(FeatureSuggestion).order_by(FeatureSuggestion.created_at.desc()).all()
    return [{
        "id": s.id,
        "user_id": s.user_id,
        "username": s.user.username if s.user else None,
        "description": s.description,
        "status": s.status,
        "created_at": s.created_at,
    } for s in suggestions]


@router.get("/incorrect-info-reports")
def admin_list_incorrect_info_reports(
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    """List all incorrect-info reports, newest first. Requires admin role."""
    reports = db.query(IncorrectInfoReport).order_by(IncorrectInfoReport.created_at.desc()).all()
    return [{
        "id": r.id,
        "stall_id": r.stall_id,
        "user_id": r.user_id,
        "username": r.user.username if r.user else None,
        "issue_type": r.issue_type,
        "description": r.description,
        "status": r.status,
        "created_at": r.created_at,
    } for r in reports]


@router.put("/incorrect-info-reports/{report_id}/status")
def update_incorrect_info_status(
    report_id: int,
    status: str = Body(..., embed=True),
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    """Update the status of an incorrect-info report. Requires admin role."""
    report = db.query(IncorrectInfoReport).filter(IncorrectInfoReport.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    report.status = status
    db.commit()
    return {"status": status}


# ── Push Notifications ──

class BroadcastNotification(BaseModel):
    title: str
    message: str
    notification_type: str = "alert"  # alert, promo, maintenance, update


@router.post("/notifications/broadcast")
def broadcast_notification(
    data: BroadcastNotification,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    """Send a broadcast notification visible to all users. Requires admin role."""
    notif = Notification(
        user_id=None,  # Broadcast
        title=data.title,
        message=data.message,
        notification_type=data.notification_type,
    )
    db.add(notif)
    db.commit()
    return {"status": "broadcast sent"}


# ── User Management ──

@router.get("/users")
def admin_list_users(
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    """List all registered users, newest first. Requires admin role."""
    users = db.query(User).order_by(User.created_at.desc()).all()
    return [{
        "id": u.id,
        "email": u.email,
        "username": u.username,
        "role": u.role,
        "is_active": u.is_active,
        "created_at": u.created_at,
    } for u in users]


@router.put("/users/{user_id}/deactivate")
def deactivate_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    """Deactivate a user account (soft-delete). Requires admin role."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_active = False
    db.commit()
    return {"status": "deactivated"}


# ── Cuisine Type Management ──

@router.get("/cuisine-types")
def admin_list_cuisine_types(
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    """List all cuisine types alphabetically. Requires admin role."""
    return db.query(CuisineType).order_by(CuisineType.name).all()


@router.post("/cuisine-types")
def admin_add_cuisine_type(
    name: str = Body(..., embed=True),
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    """Add a new cuisine type to the system. Requires admin role."""
    ct = CuisineType(name=name)
    db.add(ct)
    db.commit()
    db.refresh(ct)
    return ct


@router.delete("/cuisine-types/{cuisine_id}")
def admin_delete_cuisine_type(
    cuisine_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    """Delete a cuisine type by ID. Requires admin role."""
    ct = db.query(CuisineType).filter(CuisineType.id == cuisine_id).first()
    if not ct:
        raise HTTPException(status_code=404, detail="Cuisine type not found")
    db.delete(ct)
    db.commit()
    return {"status": "deleted"}


# ── Sync Government Data ──

@router.post("/sync-gov-data")
async def sync_gov_data(
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    """
    Re-fetch hawker centre data from data.gov.sg and insert any new centres.
    Existing centres (matched by name) are not overwritten.
    """
    from app.services.sg_data import fetch_hawker_list, fetch_hawker_geojson, merge_hawker_data

    try:
        hawker_list = await fetch_hawker_list()
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Failed to fetch hawker list from data.gov.sg: {e}")

    try:
        geojson = await fetch_hawker_geojson()
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Failed to fetch GeoJSON from data.gov.sg: {e}")

    merged = merge_hawker_data(hawker_list, geojson)
    created = 0
    skipped = 0

    type_map = {"HC": "Hawker Centre", "MK": "Market", "MHC": "Market & Hawker Centre"}

    for centre in merged:
        if db.query(Stall).filter(Stall.name == centre["name"]).first():
            skipped += 1
            continue

        centre_type = type_map.get(centre["type_of_centre"], "Hawker Centre")
        stall = Stall(
            name=centre["name"],
            description=f'{centre_type} with {centre.get("no_of_cooked_food_stalls") or "?"} cooked food stalls. Data from NEA / data.gov.sg.',
            address=centre["address"],
            latitude=centre["latitude"],
            longitude=centre["longitude"],
            cuisine_type="Mixed / Others",
            price_range_min=3.00,
            price_range_max=8.00,
            image_url=centre.get("photo_url"),
            is_approved=True,
        )
        db.add(stall)
        created += 1

    db.commit()
    return {
        "status": "sync complete",
        "source": "data.gov.sg (NEA)",
        "total_fetched": len(merged),
        "new_centres_added": created,
        "already_existed": skipped,
    }
