"""
SavedSearch Entity  (<<entity>>)

Persists a user's named search/filter configuration (stored as JSON)
so they can quickly re-apply the same filters without re-entering them.
"""

from sqlalchemy import String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class SavedSearch(Base):
    __tablename__ = "saved_searches"

    # TODO: define columns — id (pk), user_id (fk → users), name (str), filters (JSON), created_at
    pass
