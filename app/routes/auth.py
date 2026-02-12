"""Authentication routes."""
from fastapi import APIRouter, Request, Form, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
import sys

# Add parent directory to path to import from lib
sys.path.append(str(Path(__file__).parent.parent.parent))
from p_dynamics.lib.supabase_client import get_supabase_client

templates = Jinja2Templates(directory=str(Path(__file__).parent.parent / "templates"))

router = APIRouter()


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Display login page."""
    return templates.TemplateResponse("login.html", {"request": request, "error": None, "success": None})


@router.post("/login")
async def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...)
):
    """Handle login form submission."""
    try:
        supabase = get_supabase_client()
        response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        
        if response.user and response.session:
            # Create response with redirect
            redirect = RedirectResponse(url="/test", status_code=303)
            # Set session cookie
            redirect.set_cookie(
                key="access_token",
                value=response.session.access_token,
                httponly=True,
                secure=False,  # Set to True in production with HTTPS
                samesite="lax"
            )
            redirect.set_cookie(
                key="user_id",
                value=response.user.id,
                httponly=True,
                secure=False,
                samesite="lax"
            )
            return redirect
        else:
            return templates.TemplateResponse(
                "login.html",
                {"request": request, "error": "Login failed. Please check your credentials.", "success": None}
            )
    except Exception as e:
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": f"Error: {str(e)}", "success": None}
        )


@router.post("/signup")
async def signup(
    request: Request,
    email: str = Form(...),
    password: str = Form(...)
):
    """Handle signup form submission."""
    try:
        supabase = get_supabase_client()
        response = supabase.auth.sign_up({
            "email": email,
            "password": password
        })
        
        if response.user:
            # Check if session exists (might be None if email confirmation required)
            if response.session:
                # Create response with redirect
                redirect = RedirectResponse(url="/test", status_code=303)
                # Set session cookie
                redirect.set_cookie(
                    key="access_token",
                    value=response.session.access_token,
                    httponly=True,
                    secure=False,
                    samesite="lax"
                )
                redirect.set_cookie(
                    key="user_id",
                    value=response.user.id,
                    httponly=True,
                    secure=False,
                    samesite="lax"
                )
                return redirect
            else:
                # Email confirmation required
                return templates.TemplateResponse(
                    "login.html",
                    {
                        "request": request, 
                        "error": None,
                        "success": "Cuenta creada. Por favor, verifica tu email antes de iniciar sesión."
                    }
                )
        else:
            return templates.TemplateResponse(
                "login.html",
                {"request": request, "error": "Sign up failed. Please try again.", "success": None}
            )
    except Exception as e:
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": f"Error: {str(e)}", "success": None}
        )


@router.get("/logout")
async def logout(request: Request):
    """Handle logout."""
    try:
        supabase = get_supabase_client()
        supabase.auth.sign_out()
    except:
        pass
    
    redirect = RedirectResponse(url="/auth/login")
    redirect.delete_cookie("access_token")
    redirect.delete_cookie("user_id")
    return redirect
