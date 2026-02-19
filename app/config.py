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

# Session cookie settings
SESSION_ACCESS_COOKIE = os.getenv("SESSION_ACCESS_COOKIE", "pd_access_token")
SESSION_REFRESH_COOKIE = os.getenv("SESSION_REFRESH_COOKIE", "pd_refresh_token")
COOKIE_MAX_AGE = int(os.getenv("COOKIE_MAX_AGE", "2592000"))
COOKIE_SAMESITE = os.getenv("COOKIE_SAMESITE", "lax")
COOKIE_SECURE = os.getenv("COOKIE_SECURE", "").lower() == "true" or APP_URL.startswith("https")
