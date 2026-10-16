"""
Report Entities  (<<entity>>)

BugReport, FeatureSuggestion, and IncorrectInfoReport.
Each follows a status lifecycle: pending → reviewed → resolved/implemented.
All are linked to the submitting user via user_id foreign key.
"""

from sqlalchemy import String, Text, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class BugReport(Base):
    __tablename__ = "bug_reports"

    # TODO: define columns — id (pk), user_id (fk → users), category (str),
    #       description (text), status (default "pending"), created_at
    pass


class FeatureSuggestion(Base):
    __tablename__ = "feature_suggestions"

    # TODO: define columns — id (pk), user_id (fk → users),
    #       description (text), status (default "pending"), created_at
    pass


class IncorrectInfoReport(Base):
    __tablename__ = "incorrect_info_reports"

    # TODO: define columns — id (pk), stall_id (fk → stalls), user_id (fk → users),
    #       issue_type (str), description (text), status (default "pending"), created_at
    pass
