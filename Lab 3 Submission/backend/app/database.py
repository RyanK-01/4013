"""
Database Engine & Session  (<<infrastructure>>)

Sets up the SQLAlchemy engine from the DATABASE_URL setting, creates a
session factory (SessionLocal), and provides a get_db() FastAPI dependency
that yields one session per request and closes it afterwards.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from app.config import settings


class Base(DeclarativeBase):
    """Declarative base class that all ORM models inherit from."""
    pass


# TODO: create engine from settings.DATABASE_URL, create SessionLocal sessionmaker


def get_db():
    """FastAPI dependency — yields a DB session, closes it in finally block."""
    # TODO: yield SessionLocal(), close in finally
    pass
