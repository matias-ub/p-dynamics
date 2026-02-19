"""Authentication service."""
from ..utils.supabase import get_supabase_client
from ..models import AnonymousAuthResponse


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
