"""API routes for user-submitted reports (bugs, features, incorrect info, crowd levels) and saved searches."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.report import BugReport, FeatureSuggestion, IncorrectInfoReport
from app.models.crowd_report import CrowdReport
from app.schemas.report import (
    BugReportCreate, BugReportOut,
    FeatureSuggestionCreate, FeatureSuggestionOut,
    IncorrectInfoReportCreate, IncorrectInfoReportOut,
    CrowdReportCreate, CrowdReportOut,
    SavedSearchCreate, SavedSearchOut,
)
from app.models.saved_search import SavedSearch
from app.middleware.auth import get_current_user

router = APIRouter(prefix="/api/reports", tags=["reports"])


# ── Bug Reports ──

@router.post("/bugs", response_model=BugReportOut)
def report_bug(
    data: BugReportCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Submit a bug report with category and description. Requires JWT."""
    report = BugReport(
        user_id=current_user.id,
        category=data.category,
        description=data.description,
    )
    db.add(report)
    db.commit()
    db.refresh(report)
    return report


# ── Feature Suggestions ──

@router.post("/features", response_model=FeatureSuggestionOut)
def suggest_feature(
    data: FeatureSuggestionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Submit a feature suggestion. Requires JWT."""
    suggestion = FeatureSuggestion(
        user_id=current_user.id,
        description=data.description,
    )
    db.add(suggestion)
    db.commit()
    db.refresh(suggestion)
    return suggestion


# ── Incorrect Info Reports ──

@router.post("/incorrect-info", response_model=IncorrectInfoReportOut)
def report_incorrect_info(
    data: IncorrectInfoReportCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Report incorrect stall information for a specific stall. Requires JWT."""
    report = IncorrectInfoReport(
        stall_id=data.stall_id,
        user_id=current_user.id,
        issue_type=data.issue_type,
        description=data.description,
    )
    db.add(report)
    db.commit()
    db.refresh(report)
    return report


# ── Crowd Reports ──

@router.post("/crowd", response_model=CrowdReportOut)
def submit_crowd_report(
    data: CrowdReportCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Submit a crowd-level report for a stall, pending admin approval. Requires JWT."""
    report = CrowdReport(
        stall_id=data.stall_id,
        user_id=current_user.id,
        crowd_level=data.crowd_level,
        is_approved=False,
    )
    db.add(report)
    db.commit()
    db.refresh(report)
    return report


# ── Saved Searches ──

@router.post("/saved-searches", response_model=SavedSearchOut)
def save_search(
    data: SavedSearchCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Save a named set of recommendation filters for later reuse. Requires JWT."""
    saved = SavedSearch(
        user_id=current_user.id,
        name=data.name,
        filters=data.filters,
    )
    db.add(saved)
    db.commit()
    db.refresh(saved)
    return saved


@router.get("/saved-searches", response_model=list[SavedSearchOut])
def get_saved_searches(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retrieve the current user's saved searches, newest first. Requires JWT."""
    return (
        db.query(SavedSearch)
        .filter(SavedSearch.user_id == current_user.id)
        .order_by(SavedSearch.created_at.desc())
        .all()
    )


@router.delete("/saved-searches/{search_id}")
def delete_saved_search(
    search_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete a saved search by ID. Only the owning user may delete. Requires JWT."""
    saved = (
        db.query(SavedSearch)
        .filter(SavedSearch.id == search_id, SavedSearch.user_id == current_user.id)
        .first()
    )
    if not saved:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Saved search not found")
    db.delete(saved)
    db.commit()
    return {"status": "deleted"}
