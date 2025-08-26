from fastapi import APIRouter, Request, Response, HTTPException, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from pydantic import BaseModel

from app.services.auth import AuthService

router = APIRouter()
templates = Jinja2Templates(directory=Path(__file__).parent.parent / "templates")


class UserCredentials(BaseModel):
    email: str
    password: str


@router.get("/login")
async def login_page(request: Request):
    """Render the login page."""
    return templates.TemplateResponse(
        "auth/login.html", {"request": request, "title": "Login"}
    )


@router.get("/signup")
async def signup_page(request: Request):
    """Render the signup page."""
    return templates.TemplateResponse(
        "auth/signup.html", {"request": request, "title": "Sign Up"}
    )


@router.post("/login")
async def login(credentials: UserCredentials, response: Response):
    """Handle login form submission."""
    auth_data = await AuthService.sign_in(credentials.email, credentials.password)
    response.set_cookie(
        key="access_token",
        value=auth_data["session"].access_token,
        httponly=True,
        secure=True,
        samesite="lax",
    )
    return {"success": True}


@router.post("/signup")
async def signup(credentials: UserCredentials, response: Response):
    """Handle signup form submission."""
    auth_data = await AuthService.sign_up(credentials.email, credentials.password)
    response.set_cookie(
        key="access_token",
        value=auth_data["session"].access_token,
        httponly=True,
        secure=True,
        samesite="lax",
    )
    return {"success": True}


@router.post("/logout")
async def logout(request: Request, response: Response):
    """Handle logout."""
    access_token = request.cookies.get("access_token")
    if access_token:
        await AuthService.sign_out(access_token)
    response.delete_cookie(key="access_token")
    return {"success": True}
