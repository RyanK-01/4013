"""
Authentication Middleware  (<<control>>)

Handles password hashing with bcrypt, JWT token creation/validation,
and provides injectable FastAPI dependencies:
  - get_current_user: requires valid JWT, returns User or 401
  - get_optional_user: returns User or None (for mixed auth endpoints)
  - require_admin: requires JWT + admin role, or 403
"""

from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
import bcrypt
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login", auto_error=False)


def hash_password(password: str) -> str:
    """Hash a plaintext password using bcrypt with a random salt."""
    # TODO: use bcrypt.hashpw to hash and return as string
    pass


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Check a plaintext password against its stored bcrypt hash."""
    # TODO: use bcrypt.checkpw to compare
    pass


def create_access_token(data: dict) -> str:
    """Create a signed JWT with an expiry based on settings. sub should be str(user.id)."""
    # TODO: copy data, add exp claim, encode with SECRET_KEY and ALGORITHM
    pass


def get_current_user(
    token: str | None = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    """Extract user from JWT bearer token. Raises 401 if missing/invalid/inactive."""
    # TODO: decode token, extract sub, look up user in DB, check is_active
    pass


def get_optional_user(
    token: str | None = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User | None:
    """Same as get_current_user but returns None for unauthenticated requests."""
    # TODO: try to decode + lookup, return None on any failure
    pass


def require_admin(current_user: User = Depends(get_current_user)) -> User:
    """Enforce admin role on top of JWT auth. Raises 403 if user is not admin."""
    # TODO: check current_user.role == "admin", raise 403 otherwise
    pass
