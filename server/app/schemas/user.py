"""Pydantic schemas for user registration, authentication, and profile responses."""

from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserCreate(BaseModel):
    """Request body for new user registration."""
    email: EmailStr
    username: str
    password: str


class UserLogin(BaseModel):
    """Credentials submitted for email/password login."""
    email: str
    password: str


class UserOut(BaseModel):
    """Public user profile returned in API responses."""
    id: int
    email: str
    username: str
    role: str
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class Token(BaseModel):
    """JWT access token returned after successful authentication."""
    access_token: str
    token_type: str = "bearer"
    user: UserOut
