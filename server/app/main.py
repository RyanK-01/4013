"""FastAPI application entry point — configures CORS, static files, and registers all route modules."""

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.database import engine, Base
from app.models import *  # noqa: F401, F403 – registers all models

from app.routes.auth import router as auth_router
from app.routes.stalls import router as stalls_router
from app.routes.recommendations import router as recommendations_router
from app.routes.reviews import router as reviews_router
from app.routes.reports import router as reports_router
from app.routes.favourites import router as favourites_router
from app.routes.notifications import router as notifications_router
from app.routes.admin import router as admin_router
from app.routes.geocode import router as geocode_router

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SC2006 Hawker Food Recommendation App",
    version="1.0.0",
    description="Backend API for hawker food stall recommendations in Singapore",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files for uploads
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

# Register routes
app.include_router(auth_router)
app.include_router(stalls_router)
app.include_router(recommendations_router)
app.include_router(reviews_router)
app.include_router(reports_router)
app.include_router(favourites_router)
app.include_router(notifications_router)
app.include_router(admin_router)
app.include_router(geocode_router)


@app.get("/")
def root():
    """Health-check endpoint that returns API metadata and data-source attributions."""
    return {
        "message": "SC2006 HawkerLah! API",
        "docs": "/docs",
        "data_sources": {
            "hawker_centres": "data.gov.sg (NEA)",
            "geocoding": "OneMap (SLA)",
        },
    }
