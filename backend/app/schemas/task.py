from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from app.models.task import TaskStatus, TaskPriority

class TaskBase(BaseModel):
    case_id: int
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    status: TaskStatus = TaskStatus.PENDING
    priority: TaskPriority = TaskPriority.MEDIUM

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    case_id: Optional[int] = None
    title: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None

class TaskInDBBase(TaskBase):
    id: int
    assigned_to: Optional[int] = None
    created_at: datetime
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class Task(TaskInDBBase):
    pass
