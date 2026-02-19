"""Question service for fetching daily questions."""
from datetime import date
from typing import List
from ..utils.supabase import get_supabase_client
from ..models import DailyQuestionResponse, QuestionOption


def get_today_daily_question() -> DailyQuestionResponse:
    """
    Get today's daily question with options.
    
    Returns:
        DailyQuestionResponse with question text and options
        
    Raises:
        Exception if no question exists for today
    """
    supabase = get_supabase_client()
    today = date.today()
    
    # Fetch daily question with related question and options
    result = supabase.table("daily_questions")\
        .select("""
            id,
            questions!inner(
                text,
                intensity_level,
                options(id, text, position)
            )
        """)\
        .eq("date", str(today))\
        .single()\
        .execute()
    
    if not result.data:
        raise Exception("No question available for today")
    
    question_data = result.data["questions"]
    
    # Sort options by position
    options = sorted(
        question_data["options"],
        key=lambda x: x["position"]
    )
    
    return DailyQuestionResponse(
        id=result.data["id"],
        text=question_data["text"],
        intensity_level=question_data["intensity_level"],
        options=[QuestionOption(**opt) for opt in options]
    )
