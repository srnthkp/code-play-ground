"""Task schemas for the application."""
from typing import Optional
from pydantic import BaseModel


class TaskBase(BaseModel):
    """Base schema for Task."""
    title: str
    description: Optional[str] = None
    priority: Optional[str] = "normal"  # e.g., "low", "normal", "high"
    assigned_to: Optional[int] = None  # User ID of the assignee
    due_date: Optional[str] = None  # ISO format date string
    # User ID of the person who assigned the task
    assigned_by: Optional[int] = None


class TaskCreate(TaskBase):
    """Schema for creating a new Task."""


class TaskUpdate(BaseModel):
    """Schema for updating an existing Task."""
    id: int
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    is_deleted: Optional[bool] = None
    modified_by: Optional[int] = None


class Task(TaskBase):
    """Schema for Task with additional fields."""
    id: int

    class Config:
        """Configuration for Task schema."""
        from_attributes = True
