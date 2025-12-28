from __future__ import annotations

"""Shared HTTP constants for the Slack channels service."""

CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type, Authorization, X-Client-Info, Apikey",
}

# These settings are compatible with FastAPI's CORSMiddleware configuration.
CORS_CONFIG = {
    "allow_origins": ["*"],
    "allow_methods": ["*"],
    "allow_headers": ["*"],
    "allow_credentials": False,
}
