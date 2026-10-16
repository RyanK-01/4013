"""
CrowdReport Entity  (<<entity>>)

User-submitted crowd level observation (0–100%) for a stall.
Requires admin approval before the crowd_level is applied to the stall.
On approval, the stall's crowd_level field is updated to match.
"""

from sqlalchemy import Integer, Boolean, Text, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class CrowdReport(Base):
    __tablename__ = "crowd_reports"

    # TODO: define columns — id (pk), stall_id (fk → stalls), user_id (fk → users),
    #       crowd_level (int 0–100), is_approved (default False), rejection_reason, created_at
    pass
