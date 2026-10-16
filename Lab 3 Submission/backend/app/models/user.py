"""
User Entity  (<<entity>>)

Registered application user with role-based access control.
Roles: "user" (standard consumer) or "admin" (moderator).
Passwords are stored as bcrypt hashes. Users can be soft-deactivated
by setting is_active = False.
"""

from sqlalchemy import String, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    # TODO: define columns — id (pk), email (unique), username (unique),
    #       hashed_password, role (default "user"), is_active (default True), created_at
    pass
