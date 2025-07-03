"""Crud operations for Task model."""
from sqlalchemy.orm import Session
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate


def get_task(db: Session, task_id: int):
    """Retrieve a task by its ID."""
    db_task = db.query(Task).filter(Task.id == task_id).first()
    return TaskUpdate(
        id=db_task.id,
        title=db_task.title,
        description=db_task.description,
        status=db_task.status,
        priority=db_task.priority,
        assigned_to=db_task.assigned_to,
        due_date=db_task.due_date,
        assigned_by=db_task.assigned_by
    )


def get_tasks(db: Session, skip: int = 0, limit: int = 100):
    """Retrieve a list of tasks with pagination."""
    db_tasks = db.query(Task).offset(skip).limit(limit).all()
    return [
        TaskUpdate(
            id=task.id,
            title=task.title,
            description=task.description,
            status=task.status,
            priority=task.priority,
            assigned_to=task.assigned_to,
            due_date=task.due_date,
            assigned_by=task.assigned_by
        )
        for task in db_tasks
    ]


def create_task(db: Session, task: TaskCreate):
    """Create a new task."""
    db_task = Task(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    created_task = TaskUpdate(
        id=db_task.id,
        title=db_task.title,
        description=db_task.description,
        status=db_task.status,
        priority=db_task.priority,
        assigned_to=db_task.assigned_to,
        due_date=db_task.due_date,
        assigned_by=db_task.assigned_by
    )
    return created_task


def update_task(db: Session, task_id: int, task: TaskUpdate, updated_by: int):
    """Update an existing task."""
    db_task = db.query(Task).filter(Task.id == task_id).first()
    db_task.modified_by = updated_by
    if not db_task:
        return None
    for key, value in task.model_dump(exclude_unset=True).items():
        setattr(db_task, key, value)
    db.commit()
    db.refresh(db_task)
    return TaskUpdate(
        id=db_task.id,
        title=db_task.title,
        description=db_task.description,
        status=db_task.status,
        priority=db_task.priority,
        assigned_to=db_task.assigned_to,
        due_date=db_task.due_date,
        assigned_by=db_task.assigned_by,
        is_deleted=db_task.is_deleted,
        modified_by=db_task.modified_by
    )
