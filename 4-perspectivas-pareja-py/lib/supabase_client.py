"""Supabase client configuration and utilities."""
import os
from typing import Optional
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")

supabase: Optional[Client] = None

def get_supabase_client() -> Client:
    """Get or create Supabase client instance."""
    global supabase
    
    if supabase is None:
        if not SUPABASE_URL or not SUPABASE_KEY:
            raise ValueError(
                "SUPABASE_URL and SUPABASE_KEY must be set in environment variables. "
                "Please check your .env file."
            )
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    return supabase
