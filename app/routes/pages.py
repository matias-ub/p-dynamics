"""SSR (Server-Side Rendering) page routes."""
from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from ..dependencies import get_optional_user, get_current_user
from ..services import room_service, question_service
from ..models import User


router = APIRouter()
templates = Jinja2Templates(directory=str(Path(__file__).parent.parent / "templates"))


@router.get("/", response_class=HTMLResponse)
async def index(request: Request, user: User = Depends(get_optional_user)):
    """Landing page with today's question."""
    # Get today's question
    try:
        question = question_service.get_today_daily_question()
    except:
        question = None
    
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "user": user, "question": question}
    )


@router.get("/join-room", response_class=HTMLResponse)
async def join_room_page(request: Request, token: str = None, error: str = None):
    """Page to join a room with a token."""
    return templates.TemplateResponse(
        "join_room.html",
        {"request": request, "token": token, "error": error}
    )


@router.get("/question/{room_id}", response_class=HTMLResponse)
async def question_page(
    request: Request,
    room_id: str,
    user: User = Depends(get_current_user)
):
    """
    Page to answer today's question.
    """
    try:
        # Get room details
        room = room_service.get_room_by_id(room_id)
        
        # Get today's question
        question = question_service.get_today_daily_question()
        
        return templates.TemplateResponse(
            "question.html",
            {
                "request": request,
                "user": user,
                "room": room,
                "question": question
            }
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
