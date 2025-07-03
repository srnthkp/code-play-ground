"""Task model for the Employment API."""
# pylint: disable=too-few-public-methods
from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from app.db.session import Base


class Task(Base):
    """Task model for the Employment API."""
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    # e.g., "pending", "in_progress", "completed"
    status = Column(String, default="pending")
    # User ID of the assignee
    assigned_to = Column(Integer, ForeignKey("users.id"), nullable=True)
    assigned_by = Column(Integer, ForeignKey("users.id"),
                         nullable=True)  # User ID of the assigner
    # Timestamp for creation
    created_at = Column(DateTime, default=datetime.now)
    # Timestamp for last modification
    modified_at = Column(
        DateTime, default=datetime.now, onupdate=datetime.now)
    # Optional due date for the task
    due_date = Column(DateTime, nullable=True)
    # e.g., "low", "normal", "high"
    priority = Column(String, default="normal")
    is_deleted = Column(Boolean, default=False)
    modified_by = Column(Integer, ForeignKey("users.id"), nullable=True)
