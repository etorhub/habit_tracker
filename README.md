# Habit Tracker

A minimalist habit tracking application built with FastAPI, HTMX, and Alpine.js.

## Tech Stack

- Backend: FastAPI + Jinja2
- Frontend: HTMX + Alpine.js
- Styling: Tailwind CSS + DaisyUI
- Database: Supabase (PostgreSQL)
- Authentication: Supabase Auth

## Development Setup

1. Install Poetry (Python package manager):

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

2. Install dependencies:

```bash
poetry install
```

3. Create a `.env` file:

```bash
cp .env.example .env
# Fill in your environment variables
```

4. Run the development server:

```bash
poetry run uvicorn app.main:app --reload
```

## Project Structure

```
habit_tracker/
├── app/
│   ├── main.py          # FastAPI application
│   ├── config.py        # Configuration management
│   ├── models/          # SQLModel/Pydantic models
│   ├── routes/          # API routes
│   ├── services/        # Business logic
│   ├── templates/       # Jinja2 templates
│   └── static/          # CSS, JS, etc.
└── tests/               # Test files
```

## Deployment

This project is configured for deployment on Railway.app.
