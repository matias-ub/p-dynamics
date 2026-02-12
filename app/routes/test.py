"""Test/quiz routes."""
from fastapi import APIRouter, Request, Form, Cookie
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from typing import Optional
import sys

# Add parent directory to path to import from lib
sys.path.append(str(Path(__file__).parent.parent.parent))
from p_dynamics.lib.scenarios import get_scenarios_legacy

templates = Jinja2Templates(directory=str(Path(__file__).parent.parent / "templates"))

router = APIRouter()

# In-memory session storage (in production, use Redis or database)
test_sessions = {}


def get_or_create_session(user_id: str):
    """Get or create a test session for a user."""
    if user_id not in test_sessions:
        test_sessions[user_id] = {
            "current_scenario_index": 0,
            "current_question_index": 0,
            "answers": {}
        }
    return test_sessions[user_id]


@router.get("", response_class=HTMLResponse)
@router.get("/", response_class=HTMLResponse)
async def test_page(request: Request, user_id: Optional[str] = Cookie(None)):
    """Display test page."""
    if not user_id:
        return RedirectResponse(url="/auth/login")
    
    session = get_or_create_session(user_id)
    scenarios = get_scenarios_legacy()
    
    # Get current scenario and question
    scenario_idx = session["current_scenario_index"]
    question_idx = session["current_question_index"]
    
    if scenario_idx >= len(scenarios):
        return RedirectResponse(url="/results")
    
    current_scenario = scenarios[scenario_idx]
    current_question = current_scenario["questions"][question_idx]
    
    # Calculate progress
    total_questions = sum(len(s["questions"]) for s in scenarios)
    answered_questions = len(session["answers"])
    progress = int((answered_questions / total_questions * 100)) if total_questions > 0 else 0
    
    return templates.TemplateResponse(
        "test.html",
        {
            "request": request,
            "scenario": current_scenario,
            "question": current_question,
            "progress": progress,
            "can_go_back": scenario_idx > 0 or question_idx > 0,
            "scenario_idx": scenario_idx,
            "question_idx": question_idx
        }
    )


@router.post("/answer")
async def submit_answer(
    request: Request,
    question_id: str = Form(...),
    answer_index: int = Form(...),
    user_id: Optional[str] = Cookie(None)
):
    """Handle answer submission."""
    if not user_id:
        return RedirectResponse(url="/auth/login")
    
    session = get_or_create_session(user_id)
    scenarios = get_scenarios_legacy()
    
    # Save answer
    session["answers"][question_id] = answer_index
    
    # Move to next question
    scenario_idx = session["current_scenario_index"]
    question_idx = session["current_question_index"]
    
    current_scenario = scenarios[scenario_idx]
    
    if question_idx < len(current_scenario["questions"]) - 1:
        # Next question in same scenario
        session["current_question_index"] += 1
    else:
        # Move to next scenario
        if scenario_idx < len(scenarios) - 1:
            session["current_scenario_index"] += 1
            session["current_question_index"] = 0
        else:
            # Test completed
            return RedirectResponse(url="/results", status_code=303)
    
    return RedirectResponse(url="/test", status_code=303)


@router.post("/previous")
async def previous_question(request: Request, user_id: Optional[str] = Cookie(None)):
    """Go to previous question."""
    if not user_id:
        return RedirectResponse(url="/auth/login")
    
    session = get_or_create_session(user_id)
    scenarios = get_scenarios_legacy()
    
    scenario_idx = session["current_scenario_index"]
    question_idx = session["current_question_index"]
    
    if question_idx > 0:
        session["current_question_index"] -= 1
    elif scenario_idx > 0:
        session["current_scenario_index"] -= 1
        prev_scenario = scenarios[session["current_scenario_index"]]
        session["current_question_index"] = len(prev_scenario["questions"]) - 1
    
    return RedirectResponse(url="/test", status_code=303)
