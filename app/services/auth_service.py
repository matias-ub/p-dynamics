"""Authentication service."""
from typing import Optional, Dict, Any
from fastapi import Response
from ..utils.supabase import get_supabase_client
from ..models import AnonymousAuthResponse, User
from ..config import (
    SESSION_ACCESS_COOKIE,
    SESSION_REFRESH_COOKIE,
    COOKIE_MAX_AGE,
    COOKIE_SAMESITE,
    COOKIE_SECURE
)


def create_anonymous_user() -> AnonymousAuthResponse:
    """
    Create an anonymous user using Supabase anonymous auth.
    
    Returns:
        AnonymousAuthResponse with user_id and tokens
    """
    supabase = get_supabase_client()
    
    # Create anonymous user
    response = supabase.auth.sign_in_anonymously()
    
    if not response.user or not response.session:
        raise Exception("Failed to create anonymous user")
    
    return AnonymousAuthResponse(
        user_id=response.user.id,
        access_token=response.session.access_token,
        refresh_token=response.session.refresh_token,
        is_anonymous=True
    )


def _build_user_from_token(access_token: str) -> User:
    supabase = get_supabase_client()
    user_response = supabase.auth.get_user(access_token)
    user = user_response.user

    if not user:
        raise Exception("Invalid access token")

    is_anon = (
        user.app_metadata.get("provider") == "anon"
        or user.email is None
    )

    return User(
        id=user.id,
        email=user.email,
        is_anonymous=is_anon,
        access_token=access_token
    )


def create_anonymous_session() -> Dict[str, Any]:
    supabase = get_supabase_client()
    response = supabase.auth.sign_in_anonymously()

    if not response.user or not response.session:
        raise Exception("Failed to create anonymous session")

    return {
        "user": User(
            id=response.user.id,
            email=response.user.email,
            is_anonymous=True,
            access_token=response.session.access_token
        ),
        "access_token": response.session.access_token,
        "refresh_token": response.session.refresh_token,
        "set_cookies": True
    }


def refresh_access_session(refresh_token: str) -> Dict[str, Any]:
    supabase = get_supabase_client()
    response = supabase.auth.refresh_session(refresh_token)

    if not response.session:
        raise Exception("Failed to refresh session")

    access_token = response.session.access_token
    new_refresh_token = response.session.refresh_token

    return {
        "user": _build_user_from_token(access_token),
        "access_token": access_token,
        "refresh_token": new_refresh_token,
        "set_cookies": True
    }


def resolve_session(
    access_token: Optional[str],
    refresh_token: Optional[str]
) -> Dict[str, Any]:
    if access_token:
        try:
            return {
                "user": _build_user_from_token(access_token),
                "access_token": access_token,
                "refresh_token": refresh_token,
                "set_cookies": False
            }
        except Exception:
            if refresh_token:
                return refresh_access_session(refresh_token)

    if refresh_token:
        try:
            return refresh_access_session(refresh_token)
        except Exception:
            return create_anonymous_session()

    return create_anonymous_session()


def apply_session_cookies(
    response: Response,
    access_token: str,
    refresh_token: str
) -> None:
    response.set_cookie(
        SESSION_ACCESS_COOKIE,
        access_token,
        httponly=True,
        max_age=COOKIE_MAX_AGE,
        samesite=COOKIE_SAMESITE,
        secure=COOKIE_SECURE,
        path="/"
    )
    response.set_cookie(
        SESSION_REFRESH_COOKIE,
        refresh_token,
        httponly=True,
        max_age=COOKIE_MAX_AGE,
        samesite=COOKIE_SAMESITE,
        secure=COOKIE_SECURE,
        path="/"
    )


def refresh_token(refresh_token: str) -> dict:
    """
    Refresh an access token using a refresh token.
    
    Args:
        refresh_token: The refresh token
        
    Returns:
        New session data with access_token and refresh_token
    """
    supabase = get_supabase_client()
    response = supabase.auth.refresh_session(refresh_token)
    
    if not response.session:
        raise Exception("Failed to refresh token")
    
    return {
        "access_token": response.session.access_token,
        "refresh_token": response.session.refresh_token
    }
