"""
User Schemas  (<<datatype>>)

Pydantic models for user registration, login credentials,
public profile responses, and JWT token wrapper.
"""

from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserCreate(BaseModel):
    """Registration request — email, username, password."""
    # TODO: define email (EmailStr), username (str), password (str)
    pass


class UserLogin(BaseModel):
    """Login request — email and password."""
    # TODO: define email (str), password (str)
    pass


class UserOut(BaseModel):
    """Public user profile returned in responses."""
    # TODO: define id, email, username, role, is_active, created_at; set from_attributes
    pass


class Token(BaseModel):
    """JWT response returned after successful login or registration."""
    # TODO: define access_token (str), token_type (str = "bearer"), user (UserOut)
    pass
