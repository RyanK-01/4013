"""
Report Routes  (<<boundary>>)

User-facing endpoints for submitting bug reports, feature suggestions,
incorrect stall info reports, crowd-level observations, and managing
saved search filter configurations. All require JWT.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.report import BugReport, FeatureSuggestion, IncorrectInfoReport
from app.models.crowd_report import CrowdReport
from app.models.saved_search import SavedSearch
from app.schemas.report import (
    BugReportCreate, BugReportOut,
    FeatureSuggestionCreate, FeatureSuggestionOut,
    IncorrectInfoReportCreate, IncorrectInfoReportOut,
    CrowdReportCreate, CrowdReportOut,
    SavedSearchCreate, SavedSearchOut,
)
from app.middleware.auth import get_current_user

router = APIRouter(prefix="/api/reports", tags=["reports"])


@router.post("/bugs", response_model=BugReportOut)
def report_bug(data: BugReportCreate, db: Session = Depends(get_db),
               current_user: User = Depends(get_current_user)):
    """File a bug report with category and description."""
    # TODO: create BugReport for current user, save to DB
    pass


@router.post("/features", response_model=FeatureSuggestionOut)
def suggest_feature(data: FeatureSuggestionCreate, db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    """Submit a feature suggestion."""
    # TODO: create FeatureSuggestion for current user, save to DB
    pass


@router.post("/incorrect-info", response_model=IncorrectInfoReportOut)
def report_incorrect_info(data: IncorrectInfoReportCreate, db: Session = Depends(get_db),
                          current_user: User = Depends(get_current_user)):
    """Report incorrect information on a specific stall."""
    # TODO: create IncorrectInfoReport for current user, save to DB
    pass


@router.post("/crowd", response_model=CrowdReportOut)
def submit_crowd_report(data: CrowdReportCreate, db: Session = Depends(get_db),
                        current_user: User = Depends(get_current_user)):
    """Submit a crowd-level observation for a stall (pending admin approval)."""
    # TODO: create CrowdReport with is_approved=False, save to DB
    pass


@router.post("/saved-searches", response_model=SavedSearchOut)
def save_search(data: SavedSearchCreate, db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):
    """Save a named filter configuration for quick reuse."""
    # TODO: create SavedSearch with current user's filters, save to DB
    pass


@router.get("/saved-searches", response_model=list[SavedSearchOut])
def get_saved_searches(db: Session = Depends(get_db),
                       current_user: User = Depends(get_current_user)):
    """List the current user's saved searches, newest first."""
    # TODO: query SavedSearch where user_id = current_user.id, order by created_at desc
    pass


@router.delete("/saved-searches/{search_id}")
def delete_saved_search(search_id: int, db: Session = Depends(get_db),
                        current_user: User = Depends(get_current_user)):
    """Delete a saved search by ID (only if owned by current user)."""
    # TODO: find saved search, verify ownership, delete or return 404
    pass
