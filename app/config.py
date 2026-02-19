"""Application configuration."""
import os
from dotenv import load_dotenv

load_dotenv()

# Supabase settings
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
ALLOW_SERVICE_ROLE_FALLBACK = os.getenv("ALLOW_SERVICE_ROLE_FALLBACK", "false").lower() == "true"

# Validate required environment variables
if not all([SUPABASE_URL, SUPABASE_ANON_KEY, SUPABASE_SERVICE_ROLE_KEY]):
    raise RuntimeError(
        "Missing required environment variables. "
        "Please set SUPABASE_URL, SUPABASE_ANON_KEY, and SUPABASE_SERVICE_ROLE_KEY"
    )

# App settings
APP_NAME = os.getenv("APP_NAME", "Parejas - Daily Question Game")
APP_URL = os.getenv("APP_URL", "").rstrip("/")
DEBUG = os.getenv("DEBUG", "false").lower() == "true"
