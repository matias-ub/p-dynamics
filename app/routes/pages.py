"""SSR (Server-Side Rendering) page routes."""
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from ..services import room_service, question_service, auth_service
from ..config import SESSION_ACCESS_COOKIE, SESSION_REFRESH_COOKIE
from ..config import APP_URL


router = APIRouter()
templates = Jinja2Templates(directory=str(Path(__file__).parent.parent / "templates"))


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Landing page with today's question."""
    # Get today's question
    try:
        question = question_service.get_today_daily_question()
    except:
        question = None

    response = templates.TemplateResponse(
        "index.html",
        {"request": request, "user": None, "question": question, "app_url": APP_URL}
    )
    return response


@router.get("/join-room", response_class=HTMLResponse)
async def join_room_page(request: Request, token: str = None, error: str = None):
    """Page to join a room with a token."""
    response = templates.TemplateResponse(
        "join_room.html",
        {
            "request": request,
            "token": token,
            "error": error,
            "app_url": APP_URL,
            "user": None
        }
    )
    return response


@router.get("/question/{room_id}", response_class=HTMLResponse)
async def question_page(
    request: Request,
    room_id: str
):
    """
    Page to answer today's question.
    """
    try:
        # Get room details
        room = room_service.get_room_by_id(room_id)
        
        # Get today's question
        question = question_service.get_today_daily_question()
        
        session = auth_service.resolve_session(
            request.cookies.get(SESSION_ACCESS_COOKIE),
            request.cookies.get(SESSION_REFRESH_COOKIE)
        )
        user = session.get("user")

        response = templates.TemplateResponse(
            "question.html",
            {
                "request": request,
                "user": user,
                "room": room,
                "question": question,
                "app_url": APP_URL
            }
        )

        if session.get("set_cookies"):
            auth_service.apply_session_cookies(
                response,
                session["access_token"],
                session["refresh_token"]
            )

        return response
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
