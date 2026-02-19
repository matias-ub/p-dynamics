"""Main FastAPI application."""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path

from .routes import pages, auth, rooms, questions, responses
from .config import APP_NAME

# Get the app directory
app_dir = Path(__file__).parent

# Create FastAPI app
app = FastAPI(
    title=APP_NAME,
    description="Daily question game for couples to connect and understand each other better",
    version="2.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory=str(app_dir / "static")), name="static")

# Include page routers (SSR)
app.include_router(pages.router, tags=["pages"])

# Include API routers
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(rooms.router, prefix="/api/rooms", tags=["rooms"])
app.include_router(questions.router, prefix="/api/questions", tags=["questions"])
app.include_router(responses.router, prefix="/api/responses", tags=["responses"])

# Special endpoint for simplified flow
from .services import auth_service, room_service

@app.post("/api/start-session")
async def start_session():
    """
    Create an anonymous user and a room in one step.
    Returns access token, refresh token, and room_id.
    """
    try:
        # Create anonymous user
        auth_response = auth_service.create_anonymous_user()
        
        # Create room
        room = room_service.create_room()
        
        return {
            "user_id": auth_response.user_id,
            "access_token": auth_response.access_token,
            "refresh_token": auth_response.refresh_token,
            "is_anonymous": True,
            "room_id": room.id,
            "room_token": room.token
        }
    except Exception as e:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=500,
            detail=f"Failed to start session: {str(e)}"
        )


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "app": APP_NAME,
        "version": "2.0.0"
    }
