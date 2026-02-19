"""Room API routes."""
from fastapi import APIRouter, HTTPException, Depends
from ..services import room_service
from ..models import RoomResponse, RoomByTokenResponse, User
from ..dependencies import get_current_user


router = APIRouter()


@router.post("", response_model=RoomResponse)
async def create_room(current_user: User = Depends(get_current_user)):
    """
    Create a new couple room.
    Returns room details including shareable token.
    """
    try:
        return room_service.create_room()
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create room: {str(e)}"
        )


@router.get("/{token}", response_model=RoomByTokenResponse)
async def get_room_by_token(token: str):
    """
    Get room details by token (used for joining).
    Public endpoint - no auth required.
    """
    try:
        return room_service.get_room_by_token(token)
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail=f"Room not found: {str(e)}"
        )


@router.get("/id/{room_id}")
async def get_room_by_id(
    room_id: str,
    current_user: User = Depends(get_current_user)
):
    """
    Get room details by ID.
    Requires authentication.
    """
    try:
        return room_service.get_room_by_id(room_id)
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail=f"Room not found: {str(e)}"
        )
