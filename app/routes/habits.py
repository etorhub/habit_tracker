from fastapi import APIRouter, Request, Response, HTTPException
from fastapi.templating import Jinja2Templates
from pathlib import Path
from datetime import date
from typing import Optional
from pydantic import BaseModel

from app.services.supabase import get_supabase_client

router = APIRouter(prefix="/habits")
templates = Jinja2Templates(directory=Path(__file__).parent.parent / "templates")


class HabitCreate(BaseModel):
    name: str
    is_good: bool
    goal_streak: Optional[int] = None


class HabitUpdate(BaseModel):
    name: Optional[str] = None
    is_good: Optional[bool] = None
    goal_streak: Optional[int] = None


@router.get("/")
async def list_habits(request: Request):
    """Show the habits management page."""
    client = get_supabase_client(request)
    habits = (
        client.table("habits")
        .select("*")
        .eq("user_id", request.state.user.id)
        .execute()
    )

    return templates.TemplateResponse(
        "habits/index.html",
        {
            "request": request,
            "title": "Manage Habits",
            "user": request.state.user,
            "habits": habits.data,
        },
    )


@router.post("/")
async def create_habit(request: Request, habit: HabitCreate):
    """Create a new habit."""
    client = get_supabase_client(request)
    try:
        result = (
            client.table("habits")
            .insert(
                {
                    **habit.model_dump(),
                    "user_id": request.state.user.id,
                    "current_streak": 0,
                    "longest_streak": 0,
                }
            )
            .execute()
        )

        if not result.data:
            raise HTTPException(status_code=400, detail="Failed to create habit")

        return result.data[0]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{habit_id}")
async def update_habit(request: Request, habit_id: int, habit: HabitUpdate):
    """Update a habit."""
    client = get_supabase_client(request)
    try:
        result = (
            client.table("habits")
            .update(habit.model_dump(exclude_unset=True))
            .eq("id", habit_id)
            .eq("user_id", request.state.user.id)
            .execute()
        )

        if not result.data:
            raise HTTPException(status_code=404, detail="Habit not found")

        return result.data[0]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{habit_id}")
async def delete_habit(request: Request, habit_id: int):
    """Delete a habit."""
    client = get_supabase_client(request)
    try:
        result = (
            client.table("habits")
            .delete()
            .eq("id", habit_id)
            .eq("user_id", request.state.user.id)
            .execute()
        )

        if not result.data:
            raise HTTPException(status_code=404, detail="Habit not found")

        return {"success": True}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{habit_id}/toggle")
async def toggle_habit(request: Request, habit_id: int):
    """Toggle a habit's completion for today."""
    client = get_supabase_client(request)
    today = date.today().isoformat()

    try:
        # Check if we already have a log for today
        existing = (
            client.table("habit_logs")
            .select("*")
            .eq("habit_id", habit_id)
            .eq("user_id", request.state.user.id)
            .eq("date", today)
            .execute()
        )

        if existing.data:
            # Toggle existing log
            log = existing.data[0]
            result = (
                client.table("habit_logs")
                .update({"completed": not log["completed"]})
                .eq("id", log["id"])
                .execute()
            )
        else:
            # Create new log
            result = (
                client.table("habit_logs")
                .insert(
                    {
                        "habit_id": habit_id,
                        "user_id": request.state.user.id,
                        "date": today,
                        "completed": True,
                    }
                )
                .execute()
            )

        if not result.data:
            raise HTTPException(status_code=400, detail="Failed to toggle habit")

        # Update streaks
        await update_streaks(client, habit_id, request.state.user.id)

        return result.data[0]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


async def update_streaks(client, habit_id: int, user_id: str):
    """Update current and longest streaks for a habit."""
    try:
        # Get habit logs ordered by date
        logs = (
            client.table("habit_logs")
            .select("*")
            .eq("habit_id", habit_id)
            .eq("user_id", user_id)
            .order("date")
            .execute()
        )

        if not logs.data:
            return

        # Calculate current streak
        current_streak = 0
        for log in reversed(logs.data):
            if log["completed"]:
                current_streak += 1
            else:
                break

        # Calculate longest streak
        longest_streak = 0
        temp_streak = 0
        for log in logs.data:
            if log["completed"]:
                temp_streak += 1
                longest_streak = max(longest_streak, temp_streak)
            else:
                temp_streak = 0

        # Update habit
        client.table("habits").update(
            {"current_streak": current_streak, "longest_streak": longest_streak}
        ).eq("id", habit_id).execute()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
