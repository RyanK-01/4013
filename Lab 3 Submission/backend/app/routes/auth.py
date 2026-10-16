"""
Authentication Routes  (<<boundary>>)

Handles user registration, email/password login, and current-user
profile retrieval. Returns JWT tokens on successful auth.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserOut, Token
from app.middleware.auth import hash_password, verify_password, create_access_token, get_current_user

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=Token)
def register(data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user — validate uniqueness, hash password, return JWT + profile."""
    # TODO: check email/username not taken, create user, generate token, return Token
    pass


@router.post("/login", response_model=Token)
def login(data: UserLogin, db: Session = Depends(get_db)):
    """Login with email/password — verify credentials, return JWT + profile."""
    # TODO: look up user by email, verify password, check is_active, return Token
    pass


@router.get("/me", response_model=UserOut)
def get_me(current_user: User = Depends(get_current_user)):
    """Return the currently authenticated user's profile (requires JWT)."""
    # TODO: return current_user
    pass
