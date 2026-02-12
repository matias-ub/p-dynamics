# FastAPI Setup Guide

## Installation

1. Install the new dependencies:
```bash
uv pip install -r requirements-fastapi.txt
```

## Running the Application

Start the FastAPI development server:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Or using uv:
```bash
uv run uvicorn app.main:app --reload
```

## Access the Application

Open your browser and navigate to:
- Application: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

## Features

- ✅ Simple login/signup with Supabase
- ✅ Session-based authentication
- ✅ Quiz/test flow with progress tracking
- ✅ Results with dimension scores
- ✅ Responsive Bootstrap UI
- ✅ HTMX for smooth interactions (optional)

## Project Structure

```
app/
  ├── main.py              # FastAPI app entry point
  ├── routes/
  │   ├── auth.py          # Login/signup routes
  │   ├── test.py          # Quiz/test routes
  │   └── results.py       # Results display
  ├── templates/           # Jinja2 templates
  │   ├── base.html
  │   ├── login.html
  │   ├── test.html
  │   └── results.html
  └── static/              # Static files (CSS, JS)
      └── css/
          └── style.css
```

## Next Steps

1. Add database persistence for test sessions (currently in-memory)
2. Add couple pairing functionality
3. Add comparison views for partners
4. Enhance results visualization with Plotly charts
5. Add email verification
6. Deploy to production (Railway, Fly.io, etc.)
