"""Response API routes."""
from fastapi import APIRouter, HTTPException, Depends
from typing import List
from ..services import response_service
from ..models import (
    ResponseCreate,
    ResponseSubmitResult,
    StreakResponse,
    User
)
from ..dependencies import get_current_user


router = APIRouter()


@router.post("", response_model=ResponseSubmitResult)
async def submit_response(
    response_data: ResponseCreate,
    current_user: User = Depends(get_current_user)
):
    """
    Submit user's answer and partner prediction.
    """
    try:
        return response_service.submit_response(
            response_data,
            current_user.id,
            current_user.access_token
        )
    except Exception as e:
        error_msg = str(e)
        status_code = 409 if "already answered" in error_msg else 400
        raise HTTPException(status_code=status_code, detail=error_msg)


@router.get("/room/{room_id}")
async def get_room_responses(
    room_id: str,
    current_user: User = Depends(get_current_user)
):
    """
    Get all responses for a room.
    User must be a participant in the room.
    """
    try:
        return response_service.get_room_responses(
            room_id,
            current_user.id,
            current_user.access_token
        )
    except Exception as e:
        status_code = 403 if "not a participant" in str(e) else 500
        raise HTTPException(status_code=status_code, detail=str(e))


@router.get("/room/{room_id}/streak", response_model=StreakResponse)
async def get_room_streak(
    room_id: str,
    current_user: User = Depends(get_current_user)
):
    """
    Get current streak for a room.
    """
    try:
        return response_service.calculate_streak(
            room_id,
            current_user.access_token
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to calculate streak: {str(e)}"
        )


@router.get("/room/{room_id}/status/{daily_question_id}")
async def check_answer_status(
    room_id: str,
    daily_question_id: str,
    current_user: User = Depends(get_current_user)
):
    """
    Check if both participants have answered today's question.
    """
    try:
        return response_service.check_both_answered(
            room_id,
            daily_question_id,
            current_user.access_token
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to check status: {str(e)}"
        )
