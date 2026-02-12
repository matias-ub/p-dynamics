"""Main FastAPI application."""
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

from .routes import auth, test, results

# Get the app directory
app_dir = Path(__file__).parent

app = FastAPI(title="P-Dynamics", description="Couple Assessment Platform")

# Mount static files
app.mount("/static", StaticFiles(directory=str(app_dir / "static")), name="static")

# Set up Jinja2 templates
templates = Jinja2Templates(directory=str(app_dir / "templates"))

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(test.router, prefix="/test", tags=["test"])
app.include_router(results.router, prefix="/results", tags=["results"])


@app.get("/")
async def root():
    """Redirect to login page."""
    return RedirectResponse(url="/auth/login")


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
