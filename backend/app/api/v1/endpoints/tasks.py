from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api import deps
from app.services import crm_service
from app.schemas.task import Task, TaskCreate, TaskUpdate
from app.models.user import User

router = APIRouter()

@router.get("/", response_model=List[Task])
def read_tasks(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve tasks assigned to current user.
    """
    tasks = crm_service.get_tasks(db, user_id=current_user.id, skip=skip, limit=limit)
    return tasks

@router.post("/", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(
    *,
    db: Session = Depends(deps.get_db),
    task_in: TaskCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new task.
    """
    task = crm_service.create_task(db, task=task_in, assigned_to=current_user.id)
    return task

@router.get("/{id}", response_model=Task)
def read_task(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get task by ID.
    """
    task = crm_service.get_task(db, task_id=id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.assigned_to != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return task

@router.put("/{id}", response_model=Task)
def update_task(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    task_in: TaskUpdate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a task.
    """
    task = crm_service.get_task(db, task_id=id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.assigned_to != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    task = crm_service.update_task(db, task_id=id, task=task_in)
    return task
