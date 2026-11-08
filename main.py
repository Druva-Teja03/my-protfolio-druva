"""
==============================================================================
FILE: main.py
==============================================================================

PURPOSE:
The master entry point for the FastAPI application.
When you launch the server (e.g. `uvicorn main:app --reload`), Python starts here.

RESPONSIBILITIES:
1. Initialize the FastAPI app instance with metadata (title, description, version).
2. Configure CORS (Cross-Origin Resource Sharing) middleware for secure communication.
3. Automatically create database tables in SQLite on application startup.
4. Mount the '/static' directory so the browser can load CSS, JS, and image files.
5. Include the application routes from 'routes.py'.
6. Provide a convenient `python main.py` runner for local development.

CONNECTED FILES:
- database.py: Provides the SQLAlchemy 'engine' and 'Base' for table creation.
- models.py: Defines database schemas (tables) that Base creates.
- routes.py: Contains the HTTP endpoints for page rendering and form submissions.
- templates/: Jinja2 HTML templates served through the routes.
- static/: Houses CSS stylesheets, client-side JavaScript, and visual assets.

BEGINNER EXPLANATION:
Think of 'main.py' as the main switchboard and power switch of an electric train.
It turns on the engine (FastAPI), links the railroad tracks (routes),
plugs in the power station (database), points to the passenger cars (static files),
and invites everyone aboard.
==============================================================================
"""

import os
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

# Import database engine and declarative Base
from database import engine, Base
# Import the route handlers
from routes import router
# Import models so SQLAlchemy registers them with Base before table creation
import models

# -----------------------------------------------------------------------------
# STEP 1: Application Setup & Metadata
# -----------------------------------------------------------------------------
app = FastAPI(
    title="Druva Teja C — Portfolio",
    description="Portfolio of Druva Teja C, a B.Tech CSE student building FastAPI backends, MySQL databases and computer-vision pipelines.",
    version="1.0.0",
    docs_url="/docs",       # Interactive Swagger API documentation
    redoc_url="/redoc"      # Alternative ReDoc API documentation
)

# -----------------------------------------------------------------------------
# STEP 2: Configure CORS Middleware
# -----------------------------------------------------------------------------
# CORS allows web browsers to make safe requests to this backend.
# In development, allowing all origins ("*") enables seamless local testing.
# For high-security environments, you can replace "*" with your specific custom domain.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------------------------------------------------------
# STEP 3: Mount Static Files Directory
# -----------------------------------------------------------------------------
# Static files are files that do not change dynamically: CSS, JavaScript, Images, and PDFs.
# This makes them accessible via URLs like: http://127.0.0.1:8000/static/css/style.css
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

# Ensure static directory exists
os.makedirs(STATIC_DIR, exist_ok=True)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


# -----------------------------------------------------------------------------
# STEP 4: Application Lifecycle Events (Startup & Shutdown)
# -----------------------------------------------------------------------------
@app.on_event("startup")
def on_startup():
    """
    Why it exists:
        Ensures all SQLite database tables exist BEFORE any user visits the site.

    What it does:
        Calls 'Base.metadata.create_all(bind=engine)'. If 'portfolio.db' or the
        'contact_submissions' table does not exist yet, SQLAlchemy automatically
        generates them in pure SQLite.

    Inputs:
        None.

    Outputs:
        None (Side effect: creates SQLite tables).
    """
    print("[INFO] Starting Druva Teja Portfolio application...")
    Base.metadata.create_all(bind=engine)
    print("[INFO] SQLite database initialized successfully at data/portfolio.db.")


# -----------------------------------------------------------------------------
# STEP 5: Register Routes
# -----------------------------------------------------------------------------
# Connect the router containing GET / and POST /contact to the main FastAPI app.
app.include_router(router)


# -----------------------------------------------------------------------------
# STEP 6: Direct Execution Entry Point
# -----------------------------------------------------------------------------
# This allows running the server directly with: python main.py
if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("  🚀 DRUVA TEJA PORTFOLIO SERVER")
    print("  Local URL:    http://127.0.0.1:8000")
    print("  API Docs:     http://127.0.0.1:8000/docs")
    print("  Health Check: http://127.0.0.1:8000/api/health")
    print("=" * 60 + "\n")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

