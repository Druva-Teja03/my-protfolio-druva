"""
==============================================================================
FILE: routes.py
==============================================================================

PURPOSE:
Defines the URL routes (endpoints) of the portfolio web application.
Handles incoming HTTP requests, coordinates data loading, manages database operations,
and returns HTML or JSON responses.

RESPONSIBILITIES:
1. Render the main portfolio page (GET /) with dynamic data from JSON files.
2. Validate and process contact form submissions (POST /contact).
3. Provide an API health-check endpoint (GET /api/health).
4. Provide structured JSON endpoints for future external consumers or mobile apps.

CONNECTED FILES:
- templates/index.html: Rendered by Jinja2 in the home route.
- database.py: Provides the 'get_db' database session dependency.
- models.py: Provides 'ContactSubmission' to save messages into SQLite.
- data/*.json: Reads content files (personal_info, projects, skills, achievements).
- main.py: Registers this router into the FastAPI application.

BEGINNER EXPLANATION:
Think of routes as the receptionist at an office.
When someone walks in asking for the home page (GET /), the receptionist
gathers all information from our data files, dresses it nicely inside
index.html, and hands it to the visitor.
When someone submits a message (POST /contact), the receptionist verifies
the message is polite and complete, writes it in the guestbook (SQLite),
and gives a friendly confirmation.
==============================================================================
"""

import os
import re
import json
from typing import Dict, Any, List
from fastapi import APIRouter, Request, Depends, HTTPException, status, BackgroundTasks
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field, field_validator
from sqlalchemy.orm import Session

from database import get_db
from models import ContactSubmission
from email_service import send_contact_email

# -----------------------------------------------------------------------------
# STEP 1: Router & Template Initialization
# -----------------------------------------------------------------------------
router = APIRouter()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
DATA_DIR = os.path.join(BASE_DIR, "data")

# Jinja2 template renderer
templates = Jinja2Templates(directory=TEMPLATES_DIR)


# -----------------------------------------------------------------------------
# STEP 2: JSON Data Loading Helper Function
# -----------------------------------------------------------------------------
def load_json_file(filename: str, default: Any = None) -> Any:
    """
    Why it exists:
        Provides a safe, reusable way to load JSON content files from the /data directory.
        If a file is missing or has a syntax error, it returns a safe default
        instead of crashing the whole server.

    What it does:
        1. Builds the absolute path to the requested JSON file in /data.
        2. Reads and parses the JSON content into native Python dicts or lists.
        3. Returns the parsed data, or 'default' if an error occurs.

    Inputs:
        filename (str): Name of the file (e.g., 'projects.json').
        default (Any): Fallback value if the file cannot be read (defaults to empty list/dict).

    Outputs:
        Parsed Python object (dict or list) representing the JSON file contents.
    """
    file_path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(file_path):
        print(f"[WARNING] Data file not found: {file_path}. Using fallback default.")
        return default if default is not None else []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as err:
        print(f"[ERROR] Failed to parse JSON in {filename}: {err}")
        return default if default is not None else []


# -----------------------------------------------------------------------------
# STEP 3: Pydantic Validation Schema for Contact Form
# -----------------------------------------------------------------------------
class ContactFormSchema(BaseModel):
    """
    Why it exists:
        Pydantic guarantees that data arriving from the user is clean, safe,
        and conforms to required types before touching the database.

    What it does:
        - Validates that 'name' is between 2 and 100 characters.
        - Validates that 'email' is formatted as a valid email (user@domain.com).
        - Validates that 'subject' is between 2 and 200 characters.
        - Validates that 'message' is between 5 and 5,000 characters.
        - Automatically trims leading/trailing whitespace.
    """
    name: str = Field(..., min_length=2, max_length=100, description="Sender's full name")
    email: str = Field(..., min_length=5, max_length=150, description="Valid sender email address")
    subject: str = Field(..., min_length=2, max_length=200, description="Subject of the message")
    message: str = Field(..., min_length=5, max_length=5000, description="Detailed message content")

    @field_validator("email")
    @classmethod
    def validate_email_format(cls, value: str) -> str:
        clean_email = value.strip().lower()
        # Clean regex to check standard email structure (name@domain.tld)
        email_pattern = r"^[\w\.-]+@([\w-]+\.)+[\w-]{2,}$"
        if not re.match(email_pattern, clean_email):
            raise ValueError("Please provide a valid email address (e.g. name@example.com).")
        return clean_email

    class Config:
        str_strip_whitespace = True


# -----------------------------------------------------------------------------
# STEP 4: Main Portfolio Route (GET /)
# -----------------------------------------------------------------------------
@router.get("/", response_class=HTMLResponse, summary="Render Portfolio Home Page")
async def render_portfolio(request: Request):
    """
    Why it exists:
        Primary entry point of the entire website. When someone visits the root URL,
        this function loads all profile, project, skill, and milestone data, and
        renders the complete premium portfolio.

    What it does:
        1. Reads 'personal_info.json', 'projects.json', 'skills.json', and 'achievements.json'.
        2. Packages them into a template context dictionary.
        3. Renders and returns 'index.html' with high-performance server-side rendering.

    Inputs:
        request (Request): Standard FastAPI request object required by Jinja2.

    Outputs:
        HTMLResponse: Fully rendered HTML web page.
    """
    personal_info = load_json_file("personal_info.json", default={})
    projects = load_json_file("projects.json", default=[])
    skills = load_json_file("skills.json", default=[])
    achievements = load_json_file("achievements.json", default=[])

    context = {
        "request": request,
        "personal_info": personal_info,
        "projects": projects,
        "skills": skills,
        "achievements": achievements,
        "current_year": 2026,
    }

    return templates.TemplateResponse(request,"index.html", context)


# -----------------------------------------------------------------------------
# STEP 5: Contact Form Submission Route (POST /contact)
# -----------------------------------------------------------------------------
@router.post("/contact", summary="Submit Contact Inquiries")
async def submit_contact(
    payload: ContactFormSchema,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Why it exists:
        Accepts messages from recruiters, mentors, and prospective collaborators.
        Persists each validated message into SQLite for long-term record-keeping.

    What it does:
        1. Validates the JSON payload against 'ContactFormSchema'.
        2. Creates a new 'ContactSubmission' database model instance.
        3. Adds and commits the record to SQLite using SQLAlchemy.
        4. Returns a success confirmation message in JSON format.

    Inputs:
        payload (ContactFormSchema): Validated input data containing name, email, subject, message.
        db (Session): SQLAlchemy database session provided by the 'get_db' dependency.

    Outputs:
        JSONResponse: {"success": True, "message": "Thank you, Druva will get back to you soon!"}
    """
    try:
        # Create new model instance
        new_submission = ContactSubmission(
            name=payload.name.strip(),
            email=payload.email.strip().lower(),
            subject=payload.subject.strip(),
            message=payload.message.strip()
        )

        # Save to database
        db.add(new_submission)
        db.commit()
        db.refresh(new_submission)

        background_tasks.add_task(
            send_contact_email,
            new_submission.name,
            new_submission.email,
            new_submission.subject,
            new_submission.message,
        )

        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "success": True,
                "message": f"Thank you, {payload.name}! Your message has been received. I will respond to {payload.email} shortly.",
                "submission_id": new_submission.id
            }
        )
    except Exception as err:
        db.rollback()
        print(f"[DATABASE ERROR] Could not save contact submission: {err}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while saving your message. Please reach out directly via email."
        )


# -----------------------------------------------------------------------------
# STEP 6: Health Check Route (GET /api/health)
# -----------------------------------------------------------------------------
@router.get("/api/health", summary="Application Health Check")
async def health_check():
    """
    Why it exists:
        Used by cloud deployment platforms (Render, Railway, UptimeRobot, Docker)
        to verify that the server is alive and functioning properly.

    What it does:
        Returns a simple JSON status indicating healthy operational state.

    Inputs:
        None.

    Outputs:
        JSON: {"status": "healthy", "service": "druva-teja-portfolio"}
    """
    return {
        "status": "healthy",
        "service": "druva-teja-portfolio",
        "version": "1.0.0"
    }


# ==============================================================================
# FUTURE ARCHITECTURE EXPANSION ROUTES
# ==============================================================================
# When you build dedicated pages or mobile apps in future years, you can
# expose these REST endpoints:
#
# @router.get("/api/projects")
# async def get_projects_api():
#     """Returns raw JSON of all projects for external consumers."""
#     return load_json_file("projects.json", default=[])
#
# @router.get("/api/skills")
# async def get_skills_api():
#     """Returns raw JSON of all skills."""
#     return load_json_file("skills.json", default=[])
#
# @router.get("/blog")
# async def render_blog_list(request: Request):
#     """Future route: Render list of technical blog articles."""
#     return templates.TemplateResponse("blog.html", {"request": request})

