from fastapi import FastAPI, Request, Query
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
from datetime import date, datetime

from app.routes import auth, habits
from app.middleware.auth import auth_middleware
from app.services.auth import AuthService
from app.services.supabase import get_supabase

# Create FastAPI app
app = FastAPI(
    title="Habit Tracker",
    description="A minimalist habit tracking application",
    version="0.1.0",
)

# Setup static files
static_path = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=static_path), name="static")

# Setup templates
templates = Jinja2Templates(directory=Path(__file__).parent / "templates")

# Include routers
app.include_router(auth.router)
app.include_router(habits.router)

# Add middleware
app.middleware("http")(auth_middleware)


@app.get("/")
async def home(
    request: Request,
    date: str = Query(default=None, description="Date to view habits for (YYYY-MM-DD)"),
):
    """Render the home page with daily habit tracking."""
    if not request.state.user:
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "title": "Habit Tracker", "user": None},
        )

    # Use provided date or today
    view_date = date or datetime.now().date().isoformat()

    # Get all habits and their logs for the specified date
    client = get_supabase()
    habits = (
        client.table("habits")
        .select("*, habit_logs!inner(*)")
        .eq("user_id", request.state.user.id)
        .eq("habit_logs.date", view_date)
        .execute()
    )

    # If no logs exist for this date, get just the habits
    if not habits.data:
        habits = (
            client.table("habits")
            .select("*")
            .eq("user_id", request.state.user.id)
            .execute()
        )

    # Organize habits by type and add log data
    good_habits = []
    bad_habits = []

    for habit in habits.data:
        # Extract log if it exists
        log = (
            habit.get("habit_logs", [None])[0]
            if isinstance(habit.get("habit_logs"), list)
            else None
        )
        habit_data = {**habit}
        if "habit_logs" in habit_data:
            del habit_data["habit_logs"]
        habit_data["log"] = log

        if habit["is_good"]:
            good_habits.append(habit_data)
        else:
            bad_habits.append(habit_data)

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "title": "Habit Tracker",
            "user": request.state.user,
            "date": view_date,
            "good_habits": good_habits,
            "bad_habits": bad_habits,
        },
    )


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
