"""Room service for business logic."""
import os
from typing import Dict, Any
from ..utils.supabase import get_supabase_client
from ..models import RoomResponse, RoomByTokenResponse


def create_room() -> RoomResponse:
    """
    Create a new couple room with a unique token.
    
    Returns:
        RoomResponse with room details
    """
    supabase = get_supabase_client(use_service_role=True)
    
    # Generate unique token (24 chars, uppercase hex)
    token = os.urandom(12).hex().upper()
    
    room_data = {
        "token": token,
        "room_type": "couple",
        "max_participants": 2,
        "is_permanent": False,
        "streak_count": 0
    }
    
    result = supabase.table("rooms").insert(room_data).execute()
    
    if not result.data:
        raise Exception("Failed to create room")
    
    room = result.data[0]
    
    return RoomResponse(
        id=room["id"],
        token=room["token"],
        room_type=room["room_type"],
        is_permanent=room["is_permanent"],
        max_participants=room["max_participants"],
        streak_count=room.get("streak_count", 0)
    )


def get_room_by_token(token: str) -> RoomByTokenResponse:
    """
    Get room details by token (used for joining).
    
    Args:
        token: The room token
        
    Returns:
        RoomByTokenResponse with room details
        
    Raises:
        Exception if token is invalid
    """
    supabase = get_supabase_client()
    
    result = supabase.table("rooms")\
        .select("id, token, room_type, is_permanent, max_participants")\
        .eq("token", token)\
        .single()\
        .execute()
    
    if not result.data:
        raise Exception("Invalid room token")
    
    return RoomByTokenResponse(**result.data)


def get_room_by_id(room_id: str) -> Dict[str, Any]:
    """
    Get room details by ID.
    
    Args:
        room_id: The room UUID
        
    Returns:
        Room data dictionary
        
    Raises:
        Exception if room not found
    """
    supabase = get_supabase_client()
    
    result = supabase.table("rooms")\
        .select("*")\
        .eq("id", room_id)\
        .single()\
        .execute()
    
    if not result.data:
        raise Exception("Room not found")
    
    return result.data
