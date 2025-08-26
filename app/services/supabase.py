from functools import lru_cache
from supabase import create_client, Client
from fastapi import Request
from app.config import get_settings


@lru_cache()
def get_supabase() -> Client:
    """Get a cached Supabase client instance."""
    settings = get_settings()
    return create_client(settings.supabase_url, settings.supabase_key)


def get_supabase_client(request: Request) -> Client:
    """Get a Supabase client with the user's session."""
    settings = get_settings()
    client = create_client(settings.supabase_url, settings.supabase_key)

    # Set auth session if user is authenticated
    access_token = request.cookies.get("access_token")
    refresh_token = request.cookies.get("refresh_token")

    if access_token and refresh_token:
        client.auth.set_session(access_token=access_token, refresh_token=refresh_token)

    return client
