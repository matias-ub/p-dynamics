"""Authentication API routes."""
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from ..services import auth_service, room_service
from ..models import AnonymousAuthResponse


router = APIRouter()


class RefreshTokenRequest(BaseModel):
    refresh_token: str


@router.post("/anonymous", response_model=AnonymousAuthResponse)
async def create_anonymous_user():
    """
    Create an anonymous user account.
    Returns access token and refresh token.
    """
    try:
        return auth_service.create_anonymous_user()
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create anonymous user: {str(e)}"
        )


@router.post("/refresh")
async def refresh_access_token(request: RefreshTokenRequest):
    """
    Refresh an access token using a refresh token.
    """
    try:
        return auth_service.refresh_token(request.refresh_token)
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail=f"Failed to refresh token: {str(e)}"
        )
