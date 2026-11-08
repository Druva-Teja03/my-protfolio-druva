"""
==============================================================================
FILE: database.py
==============================================================================

PURPOSE:
Configures the SQLite database engine and SQLAlchemy session management.
It establishes how our Python application communicates with the database file.

RESPONSIBILITIES:
1. Define the database file path (stores data inside data/portfolio.db).
2. Create the SQLAlchemy Engine object (the connection pool).
3. Create the SessionLocal class (creates individual database sessions).
4. Provide a 'get_db' dependency function for FastAPI route handlers.

CONNECTED FILES:
- models.py: Uses the 'Base' declarative class defined here to create database tables.
- routes.py: Imports 'get_db' to read and write contact submissions during API calls.
- main.py: Imports 'engine' and 'Base' to automatically create database tables on startup.

BEGINNER EXPLANATION:
Think of the database engine as the telephone wire connecting Python to SQLite.
A "Session" is a single telephone call where you read or write records.
Once the call is done, we hang up (close the session) so memory isn't wasted.
==============================================================================
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# -----------------------------------------------------------------------------
# STEP 1: Determine the Database Location
# -----------------------------------------------------------------------------
# We want the SQLite database file to live inside the "data" folder:
# data/portfolio.db
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

# Create the data folder if it doesn't already exist
os.makedirs(DATA_DIR, exist_ok=True)

# SQLite Connection String format: sqlite:///relative_or_absolute_path
DB_FILE_PATH = os.path.join(DATA_DIR, "portfolio.db")
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_FILE_PATH}"

# -----------------------------------------------------------------------------
# STEP 2: Create the SQLAlchemy Engine
# -----------------------------------------------------------------------------
# The engine is the core interface to the database.
# 'check_same_thread: False' is required ONLY for SQLite because SQLite by default
# prevents multiple threads from sharing the same connection. FastAPI uses multiple
# worker threads to handle requests quickly, so this setting allows safe multithreading.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# -----------------------------------------------------------------------------
# STEP 3: Create the Session Factory
# -----------------------------------------------------------------------------
# SessionLocal is a factory that produces new Database Session objects on demand.
# autocommit=False: We explicitly call db.commit() when we are sure data is valid.
# autoflush=False: Prevents automatic pushes to the database before we are ready.
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# -----------------------------------------------------------------------------
# STEP 4: Create the Declarative Base
# -----------------------------------------------------------------------------
# Base is the parent class from which all database models (tables) inherit.
# SQLAlchemy inspects subclasses of Base to know what tables to create in SQLite.
Base = declarative_base()


# -----------------------------------------------------------------------------
# STEP 5: Dependency Function for FastAPI Routes
# -----------------------------------------------------------------------------
def get_db():
    """
    Why it exists:
        Provides an isolated, clean database session for each incoming HTTP request.

    What it does:
        1. Opens a new database session.
        2. Yields (lends) the session to the requesting route function.
        3. Guarantees that the session is closed when the request finishes,
           even if an error occurs.

    Inputs:
        None.

    Outputs:
        Yields an active SQLAlchemy Session instance.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        # This code ALWAYS runs after the route finishes responding
        db.close()

