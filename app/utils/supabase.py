"""Supabase client utilities."""
from supabase import create_client, Client
from ..config import SUPABASE_URL, SUPABASE_ANON_KEY, SUPABASE_SERVICE_ROLE_KEY


def get_supabase_client(use_service_role: bool = False) -> Client:
    """
    Get Supabase client instance.
    
    Args:
        use_service_role: If True, uses service role key (bypasses RLS).
                         If False, uses anon key (enforces RLS).
    
    Returns:
        Configured Supabase client
    """
    key = SUPABASE_SERVICE_ROLE_KEY if use_service_role else SUPABASE_ANON_KEY
    return create_client(SUPABASE_URL, key)


def get_supabase_authed_client(access_token: str) -> Client:
    """
    Get Supabase client instance authenticated with a user access token.
    This ensures PostgREST receives the JWT for RLS.
    """
    supabase = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
    supabase.auth.set_session(access_token=access_token, refresh_token="")
    supabase.postgrest.auth(access_token)
    return supabase
