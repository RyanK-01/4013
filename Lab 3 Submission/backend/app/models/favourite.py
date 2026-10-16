"""
Favourite Entity  (<<entity>>)

Join table tracking a user's bookmarked stalls.
Enforces a unique constraint on (user_id, stall_id) so each
user can only favourite a given stall once.
"""

from sqlalchemy import DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Favourite(Base):
    __tablename__ = "favourites"

    # TODO: define columns — id (pk), user_id (fk → users), stall_id (fk → stalls), created_at
    # TODO: add UniqueConstraint("user_id", "stall_id")
    pass
