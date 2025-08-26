from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path

from app.routes import auth
from app.services.auth import AuthService

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


@app.middleware("http")
async def inject_user(request: Request, call_next):
    """Inject the current user into the request state."""
    request.state.user = AuthService.get_user_from_cookie(request)
    response = await call_next(request)
    return response


@app.get("/")
async def home(request: Request):
    """Render the home page."""
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "title": "Habit Tracker", "user": request.state.user},
    )


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
