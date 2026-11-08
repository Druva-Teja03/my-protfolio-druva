"""
==============================================================================
FILE: models.py
==============================================================================

PURPOSE:
Defines the database tables as Python classes using SQLAlchemy ORM
(Object Relational Mapping).

RESPONSIBILITIES:
1. Define the 'ContactSubmission' table schema for storing website contact messages.
2. Map Python object attributes to SQLite table columns and data types.
3. Provide a structured foundation for future expansion tables (e.g., Blog, Analytics).

CONNECTED FILES:
- database.py: Imports 'Base', which registers this model with SQLAlchemy.
- routes.py: Uses 'ContactSubmission' to create and save new database records.
- main.py: Uses 'Base.metadata.create_all' to create the actual SQLite tables.

BEGINNER EXPLANATION:
Without an ORM, you would have to write raw SQL strings like:
"INSERT INTO contact_submissions (name, email) VALUES ('Druva', 'test@example.com')"
With SQLAlchemy ORM, you can simply write:
new_contact = ContactSubmission(name='Druva', email='test@example.com')
db.add(new_contact)
db.commit()
This makes your Python code cleaner, safer, and immune to SQL injection attacks!
==============================================================================
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from database import Base


# ==============================================================================
# MODEL 1: Contact Submissions
# ==============================================================================
class ContactSubmission(Base):
    """
    Why it exists:
        Stores every message sent through the website's contact form into SQLite.
        Recruiters, mentors, and collaborators can leave a message, and Druva can
        review all inquiries safely in the database.

    Table Name:
        contact_submissions

    Columns:
        id: Unique numeric identifier for each message (Primary Key, auto-incrementing).
        name: Full name of the person contacting.
        email: Email address so Druva can reply.
        subject: Topic of the inquiry (e.g., 'Internship Opportunity', 'Hackathon Collaboration').
        message: The actual message content.
        created_at: Exact timestamp when the message was submitted (UTC).
        is_read: Status flag (False by default) to track whether Druva has viewed it.
    """
    __tablename__ = "contact_submissions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), nullable=False, index=True)
    subject = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    is_read = Column(Boolean, default=False, nullable=False)

    def __repr__(self):
        """
        Why it exists:
            Provides a friendly string representation when debugging in Python console.
        """
        return f"<ContactSubmission id={self.id} name='{self.name}' email='{self.email}'>"


# ==============================================================================
# FUTURE ARCHITECTURE EXPANSION STUBS
# ==============================================================================
# In future years, when you want to add a blog or visitor counter, you can
# easily uncomment and build upon these models:
#
# class BlogPost(Base):
#     __tablename__ = "blog_posts"
#     id = Column(Integer, primary_key=True, index=True)
#     slug = Column(String(100), unique=True, index=True)
#     title = Column(String(250), nullable=False)
#     summary = Column(String(400))
#     content = Column(Text, nullable=False)
#     published_at = Column(DateTime, default=datetime.utcnow)
#     is_published = Column(Boolean, default=True)
#
# class VisitorAnalytic(Base):
#     __tablename__ = "visitor_analytics"
#     id = Column(Integer, primary_key=True, index=True)
#     path = Column(String(200), nullable=False)
#     timestamp = Column(DateTime, default=datetime.utcnow)
#     user_agent = Column(String(255))

