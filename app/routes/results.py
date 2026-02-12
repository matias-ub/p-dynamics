"""Results routes."""
from fastapi import APIRouter, Request, Cookie
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

# Import test sessions from test module
from .test import test_sessions


@router.get("", response_class=HTMLResponse)
@router.get("/", response_class=HTMLResponse)
async def results_page(request: Request, user_id: Optional[str] = Cookie(None)):
    """Display results page."""
    if not user_id:
        return RedirectResponse(url="/auth/login")
    
    if user_id not in test_sessions:
        return RedirectResponse(url="/test")
    
    session = test_sessions[user_id]
    answers = session["answers"]
    
    # Calculate results
    scenarios = get_scenarios_legacy()
    
    # Aggregate tag scores
    tag_scores = {}
    
    for scenario in scenarios:
        for question in scenario["questions"]:
            question_id = question["id"]
            if question_id in answers:
                answer_idx = answers[question_id]
                if answer_idx < len(question["options"]):
                    option = question["options"][answer_idx]
                    tags = option.get("tags", {})
                    
                    for tag, score in tags.items():
                        if tag not in tag_scores:
                            tag_scores[tag] = []
                        tag_scores[tag].append(score)
    
    # Calculate averages
    avg_scores = {
        tag: round(sum(scores) / len(scores), 1)
        for tag, scores in tag_scores.items()
    }
    
    # Sort by score descending
    sorted_scores = sorted(avg_scores.items(), key=lambda x: x[1], reverse=True)
    
    return templates.TemplateResponse(
        "results.html",
        {
            "request": request,
            "scores": sorted_scores,
            "total_answers": len(answers)
        }
    )


@router.post("/reset")
async def reset_test(request: Request, user_id: Optional[str] = Cookie(None)):
    """Reset the test and start over."""
    if user_id and user_id in test_sessions:
        del test_sessions[user_id]
    
    return RedirectResponse(url="/test", status_code=303)
