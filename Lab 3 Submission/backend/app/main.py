"""
FastAPI Application Entry Point  (<<infrastructure>>)

Creates the FastAPI app, configures CORS for the frontend dev server,
mounts the /uploads directory for static file serving, registers all
database tables, and includes every route module.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.database import engine, Base
from app.models import *  # noqa — registers all ORM models with SQLAlchemy

from app.routes.auth import router as auth_router
from app.routes.stalls import router as stalls_router
from app.routes.recommendations import router as recommendations_router
from app.routes.reviews import router as reviews_router
from app.routes.reports import router as reports_router
from app.routes.favourites import router as favourites_router
from app.routes.notifications import router as notifications_router
from app.routes.admin import router as admin_router
from app.routes.geocode import router as geocode_router

# TODO: call Base.metadata.create_all to create tables
# TODO: instantiate FastAPI app with title/version/description
# TODO: add CORSMiddleware allowing frontend origins
# TODO: mount /uploads as static files
# TODO: include_router for all 9 route modules
# TODO: add GET / health-check endpoint
