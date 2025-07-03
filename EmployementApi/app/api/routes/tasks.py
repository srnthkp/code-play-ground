"""This module defines the API routes for managing tasks in the Employment API."""
from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.api import deps
from app.schemas.task import TaskCreate, TaskUpdate
from app.crud import task as crud_task

router = APIRouter()


class TaskResponse(BaseModel):
    """Response model for delete task."""
    success: bool
    message: str
    task: TaskUpdate


class TasksResponse(BaseModel):
    """Response model for delete task."""
    success: bool
    message: str
    task: List[TaskUpdate]


@router.get("/read_tasks", response_model=TasksResponse)
def read_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(deps.get_db)):
    """Retrieve a list of tasks with pagination."""
    tasks = crud_task.get_tasks(db, skip=skip, limit=limit)
    if tasks is None:
        raise HTTPException(status_code=404, detail="Tasks are not found")
    return TasksResponse(
        success=True,
        message="Task read successfully",
        task=tasks
    )


@router.get("/read_task/{task_id}", response_model=TaskResponse)
def read_task(task_id: int, db: Session = Depends(deps.get_db)):
    """Retrieve a task by its ID."""
    existing_task = crud_task.get_task(db, task_id=task_id)
    if existing_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return TaskResponse(
        success=True,
        message="Task read successfully",
        task=existing_task
    )


@router.post("/create_task", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate, db: Session = Depends(deps.get_db),
                current_user=Depends(deps.require_login)):
    """Create a new task."""
    try:
        # Assuming current_user is a dict with user info
        logged_in_user = deps.get_current_user_from_payload(
            db=db, payload=current_user)
        # Set the user who created the task
        task.assigned_by = logged_in_user.id
        new_task = crud_task.create_task(db=db, task=task)
        if new_task is None:
            raise HTTPException(status_code=400, detail="Task creation failed")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating task: {str(e)}"
        ) from e
    return TaskResponse(
        success=True,
        message="Task created successfully",
        task=new_task
    )


@router.put("/update_task/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task: TaskUpdate, db: Session = Depends(deps.get_db),
                current_user=Depends(deps.require_login)):
    """Update an existing task."""
    updated_task = crud_task.update_task(db, task_id, task, deps.get_current_user_from_payload(
        db=db, payload=current_user).id)
    if updated_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return TaskResponse(
        success=True,
        message="Task updated successfully",
        task=updated_task
    )


@router.delete("/delete_task/{task_id}", response_model=TaskResponse)
def delete_task(task_id: int, db: Session = Depends(deps.get_db),
                current_user=Depends(deps.require_login)):
    """Delete a task by its ID."""
    existing_task = crud_task.get_task(db, task_id)
    if existing_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    existing_task.is_deleted = True
    deleted_task = crud_task.update_task(
        db,
        task_id,
        existing_task,
        deps.get_current_user_from_payload(db=db, payload=current_user).id)
    return TaskResponse(
        success=True,
        message="Task deleted successfully",
        task=deleted_task
    )
