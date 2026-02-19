"""Pydantic models for request/response validation."""
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import date


# ====================== User Models ======================
class User(BaseModel):
    """Authenticated user model."""
    id: str
    email: Optional[str] = None
    is_anonymous: bool
    access_token: str


# ====================== Room Models ======================
class RoomCreate(BaseModel):
    """Request model for creating a room."""
    pass  # No fields needed, all generated server-side


class RoomResponse(BaseModel):
    """Response model for room data."""
    id: str
    token: str
    room_type: str
    is_permanent: bool
    max_participants: int
    streak_count: int = 0


class RoomByTokenResponse(BaseModel):
    """Response when fetching room by token."""
    id: str
    token: str
    room_type: str
    is_permanent: bool
    max_participants: int


# ====================== Question Models ======================
class QuestionOption(BaseModel):
    """Option for a question."""
    id: str
    text: str
    position: int


class DailyQuestionResponse(BaseModel):
    """Response model for daily question."""
    id: str
    text: str
    intensity_level: int
    options: List[QuestionOption]


# ====================== Response Models ======================
class ResponseCreate(BaseModel):
    """Request model for submitting a response."""
    room_id: str
    daily_question_id: str
    self_option_id: str
    partner_prediction_option_id: str


class ResponseSubmitResult(BaseModel):
    """Response after submitting an answer."""
    status: str
    response_id: str
    message: Optional[str] = None


class ResponseDetail(BaseModel):
    """Detailed response data."""
    id: str
    room_id: str
    user_id: str
    daily_question_id: str
    self_option_id: str
    partner_prediction_option_id: str
    created_at: str
    user_name: Optional[str] = None
    self_option_text: Optional[str] = None
    prediction_option_text: Optional[str] = None


class StreakResponse(BaseModel):
    """Response model for streak data."""
    streak: int
    room_id: str


# ====================== Anonymous Auth Models ======================
class AnonymousAuthResponse(BaseModel):
    """Response after creating anonymous user."""
    user_id: str
    access_token: str
    refresh_token: str
    is_anonymous: bool
