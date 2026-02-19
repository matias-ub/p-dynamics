"""Question API routes."""
from fastapi import APIRouter, HTTPException
from ..services import question_service
from ..models import DailyQuestionResponse


router = APIRouter()


@router.get("/today", response_model=DailyQuestionResponse)
async def get_today_question():
    """
    Get today's daily question with options.
    Public endpoint - no auth required.
    """
    try:
        return question_service.get_today_daily_question()
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail=f"No question available: {str(e)}"
        )
