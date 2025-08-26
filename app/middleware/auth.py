from typing import Optional
from fastapi import Request
from fastapi.responses import RedirectResponse
from app.services.auth import AuthService


async def auth_middleware(request: Request, call_next):
    """Middleware to handle authentication and user state."""
    # Skip auth for public routes
    public_paths = {"/login", "/signup", "/static", "/health"}
    if any(request.url.path.startswith(path) for path in public_paths):
        return await call_next(request)

    # Get user from cookie
    user = AuthService.get_user_from_cookie(request)

    # Redirect to login if no user and not accessing public routes
    if not user:
        return RedirectResponse(url="/login", status_code=303)

    # Add user to request state
    request.state.user = user
    response = await call_next(request)
    return response
