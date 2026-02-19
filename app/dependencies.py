"""FastAPI dependencies."""
from fastapi import Header, HTTPException, Cookie
from typing import Optional
from .models import User
from .utils.supabase import get_supabase_client


async def get_current_user(
    authorization: Optional[str] = Header(None),
    access_token: Optional[str] = Cookie(None)
) -> User:
    """
    Get current authenticated user from JWT token.
    Supports both Authorization header and cookie-based auth.
    """
    token = None
    
    # Try Authorization header first
    if authorization and authorization.startswith("Bearer "):
        token = authorization.split(" ")[1]
    # Fallback to cookie
    elif access_token:
        token = access_token
    
    if not token:
        raise HTTPException(
            status_code=401,
            detail="Authentication required. Please provide a valid token."
        )
    
    try:
        supabase = get_supabase_client()
        
        # Verify JWT and get user
        user_response = supabase.auth.get_user(token)
        user = user_response.user
        
        if not user:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        # Set session context for RLS (important for database queries)
        # Note: We don't need refresh_token for get operations
        supabase.postgrest.auth(token)
        
        # Detect if user is anonymous
        is_anon = (
            user.app_metadata.get("provider") == "anon" 
            or user.email is None
        )
        
        return User(
            id=user.id,
            email=user.email,
            is_anonymous=is_anon
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=401, 
            detail=f"Token validation failed: {str(e)}"
        )


async def get_optional_user(
    authorization: Optional[str] = Header(None),
    access_token: Optional[str] = Cookie(None)
) -> Optional[User]:
    """
    Get current user if authenticated, None otherwise.
    Useful for pages that work for both authenticated and anonymous users.
    """
    try:
        return await get_current_user(authorization, access_token)
    except HTTPException:
        return None
