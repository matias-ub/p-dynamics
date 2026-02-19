"""FastAPI dependencies."""
from fastapi import Header, HTTPException, Response, Cookie
from typing import Optional
from .models import User
from .config import DEBUG, SESSION_ACCESS_COOKIE, SESSION_REFRESH_COOKIE
from .services import auth_service


async def get_current_user(
    response: Response,
    authorization: Optional[str] = Header(None),
    access_token: Optional[str] = Header(None, alias="X-Access-Token"),
    access_cookie: Optional[str] = Cookie(None, alias=SESSION_ACCESS_COOKIE),
    refresh_cookie: Optional[str] = Cookie(None, alias=SESSION_REFRESH_COOKIE)
) -> User:
    token = None

    # Prioritize Authorization header (standard)
    if authorization and authorization.startswith("Bearer "):
        token = authorization.split(" ")[1]
    # Fallback for HTMX or custom header
    elif access_token:
        token = access_token

    try:
        session = auth_service.resolve_session(token or access_cookie, refresh_cookie)
        user = session.get("user")
        if not user:
            raise HTTPException(status_code=401, detail="Token invalido")

        if session.get("set_cookies"):
            auth_service.apply_session_cookies(
                response,
                session["access_token"],
                session["refresh_token"]
            )

        return user
    except Exception as e:
        if DEBUG:
            print(f"[DEBUG] Token validation failed: {str(e)}")
        raise HTTPException(
            status_code=401,
            detail=f"Error al validar token: {str(e)}"
        )


async def get_optional_user(
    response: Response,
    authorization: Optional[str] = Header(None),
    access_token: Optional[str] = Header(None, alias="X-Access-Token"),
    access_cookie: Optional[str] = Cookie(None, alias=SESSION_ACCESS_COOKIE),
    refresh_cookie: Optional[str] = Cookie(None, alias=SESSION_REFRESH_COOKIE)
) -> Optional[User]:
    """
    Get current user if authenticated, None otherwise.
    Useful for pages that work for both authenticated and anonymous users.
    """
    try:
        return await get_current_user(
            response,
            authorization,
            access_token,
            access_cookie,
            refresh_cookie
        )
    except HTTPException:
        return None
