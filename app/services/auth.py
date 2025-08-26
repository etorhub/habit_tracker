from typing import Optional, Any
from fastapi import HTTPException, Request
from app.services.supabase import get_supabase


class AuthService:
    @staticmethod
    def get_user_from_cookie(request: Request) -> Optional[dict[str, Any]]:
        """Get the current user from the session cookie."""
        access_token = request.cookies.get("access_token")
        if not access_token:
            return None

        try:
            client = get_supabase()
            response = client.auth.get_user(access_token)
            return response.user
        except Exception:
            return None

    @staticmethod
    async def sign_up(email: str, password: str) -> dict[str, Any]:
        """Sign up a new user."""
        try:
            client = get_supabase()
            response = client.auth.sign_up({"email": email, "password": password})
            if not response.session:
                raise HTTPException(status_code=400, detail="Sign up failed")
            return {"user": response.user, "session": response.session}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    @staticmethod
    async def sign_in(email: str, password: str) -> dict[str, Any]:
        """Sign in an existing user."""
        try:
            client = get_supabase()
            response = client.auth.sign_in_with_password(
                {"email": email, "password": password}
            )
            if not response.session:
                raise HTTPException(status_code=400, detail="Invalid credentials")
            return {"user": response.user, "session": response.session}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    @staticmethod
    async def sign_out(access_token: str) -> None:
        """Sign out the current user."""
        try:
            client = get_supabase()
            client.auth.sign_out(access_token)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
