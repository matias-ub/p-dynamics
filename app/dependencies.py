"""FastAPI dependencies."""
from fastapi import Header, HTTPException
from typing import Optional
from .models import User
from .utils.supabase import get_supabase_client
from .config import DEBUG


async def get_current_user(
    authorization: Optional[str] = Header(None),
    access_token: Optional[str] = Header(None, alias="X-Access-Token")
) -> User:
    token = None

    # Prioritize Authorization header (standard)
    if authorization and authorization.startswith("Bearer "):
        token = authorization.split(" ")[1]
    # Fallback for HTMX or custom header
    elif access_token:
        token = access_token

    if not token:
        raise HTTPException(
            status_code=401,
            detail="Se requiere token (Bearer o X-Access-Token)"
        )

    try:
        supabase = get_supabase_client()

        # 1. Validate JWT (works for anonymous users)
        user_response = supabase.auth.get_user(token)
        user = user_response.user

        if not user:
            raise HTTPException(status_code=401, detail="Token invalido")

        # 2. Set session so RLS works for anonymous users
        supabase.auth.set_session(
            access_token=token,
            refresh_token=""
        )

        # Detect anonymous
        is_anon = (
            user.app_metadata.get("provider") == "anon"
            or user.email is None
        )

        return User(
            id=user.id,
            email=user.email,
            is_anonymous=is_anon,
            access_token=token
        )

    except Exception as e:
        if DEBUG:
            print(f"[DEBUG] Token validation failed: {str(e)}")
        raise HTTPException(
            status_code=401,
            detail=f"Error al validar token: {str(e)}"
        )


async def get_optional_user(
    authorization: Optional[str] = Header(None),
    access_token: Optional[str] = Header(None, alias="X-Access-Token")
) -> Optional[User]:
    """
    Get current user if authenticated, None otherwise.
    Useful for pages that work for both authenticated and anonymous users.
    """
    try:
        return await get_current_user(authorization, access_token)
    except HTTPException:
        return None
