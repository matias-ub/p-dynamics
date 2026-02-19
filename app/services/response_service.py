"""Response service for handling user responses and streak calculation."""
from datetime import date, timedelta
from collections import defaultdict
from typing import List, Dict, Any
from ..utils.supabase import get_supabase_client
from ..models import ResponseCreate, ResponseSubmitResult, StreakResponse


def submit_response(
    response_data: ResponseCreate,
    user_id: str
) -> ResponseSubmitResult:
    """
    Submit a user's response to a daily question.
    
    Args:
        response_data: Response data (room_id, question_id, options)
        user_id: Current user's ID
        
    Returns:
        ResponseSubmitResult with response_id
        
    Raises:
        Exception if submission fails or user already answered
    """
    supabase = get_supabase_client()
    
    payload = {
        "room_id": response_data.room_id,
        "user_id": user_id,
        "daily_question_id": response_data.daily_question_id,
        "self_option_id": response_data.self_option_id,
        "partner_prediction_option_id": response_data.partner_prediction_option_id
    }
    
    try:
        result = supabase.table("responses").insert(payload).execute()
        
        if not result.data:
            raise Exception("Failed to submit response")
        
        return ResponseSubmitResult(
            status="ok",
            response_id=result.data[0]["id"],
            message="Response submitted successfully"
        )
    except Exception as e:
        error_msg = str(e)
        if "uniq_response_per_user_day" in error_msg:
            raise Exception("You have already answered today's question in this room")
        raise Exception(f"Failed to submit response: {error_msg}")


def get_room_responses(room_id: str, user_id: str) -> List[Dict[str, Any]]:
    """
    Get all responses for a room.
    User must be a participant in the room.
    
    Args:
        room_id: Room UUID
        user_id: Current user's ID (for authorization)
        
    Returns:
        List of response dictionaries with user and option details
        
    Raises:
        Exception if user is not a participant
    """
    supabase = get_supabase_client()
    
    # Verify user is a participant
    check = supabase.table("responses")\
        .select("id")\
        .eq("room_id", room_id)\
        .eq("user_id", user_id)\
        .limit(1)\
        .execute()
    
    if not check.data:
        raise Exception("You are not a participant in this room")
    
    # Fetch all responses with joined data
    responses = supabase.table("responses")\
        .select("""
            *,
            self_option:options!self_option_id(text),
            prediction_option:options!partner_prediction_option_id(text),
            profile:profiles!user_id(name)
        """)\
        .eq("room_id", room_id)\
        .order("created_at", desc=True)\
        .execute()
    
    return responses.data if responses.data else []


def calculate_streak(room_id: str) -> StreakResponse:
    """
    Calculate current streak for a room.
    Streak = consecutive days where both participants answered.
    
    Args:
        room_id: Room UUID
        
    Returns:
        StreakResponse with current streak count
    """
    supabase = get_supabase_client()
    
    # Fetch responses from last 60 days
    today = date.today()
    start_date = today - timedelta(days=60)
    
    responses = supabase.table("responses")\
        .select("daily_question_id, user_id, created_at")\
        .eq("room_id", room_id)\
        .gte("created_at", start_date.isoformat())\
        .execute()
    
    if not responses.data:
        return StreakResponse(streak=0, room_id=room_id)
    
    # Group responses by daily_question_id (each represents one day)
    days = defaultdict(set)
    for r in responses.data:
        days[r["daily_question_id"]].add(r["user_id"])
    
    # Sort days by date (descending - most recent first)
    sorted_days = sorted(days.keys(), reverse=True)
    
    # Calculate streak (consecutive days with 2+ participants)
    streak = 0
    for dq_id in sorted_days:
        if len(days[dq_id]) >= 2:
            streak += 1
        else:
            break  # Streak broken
    
    return StreakResponse(streak=streak, room_id=room_id)


def check_both_answered(room_id: str, daily_question_id: str) -> Dict[str, Any]:
    """
    Check if both participants have answered today's question.
    
    Args:
        room_id: Room UUID
        daily_question_id: Daily question UUID
        
    Returns:
        Dictionary with status and count of answers
    """
    supabase = get_supabase_client()
    
    responses = supabase.table("responses")\
        .select("user_id")\
        .eq("room_id", room_id)\
        .eq("daily_question_id", daily_question_id)\
        .execute()
    
    count = len(responses.data) if responses.data else 0
    
    return {
        "both_answered": count >= 2,
        "answer_count": count,
        "room_id": room_id,
        "daily_question_id": daily_question_id
    }
