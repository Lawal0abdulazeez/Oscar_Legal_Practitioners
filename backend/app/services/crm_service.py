from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.client import Client
from app.models.case import Case
from app.models.task import Task
from app.schemas.client import ClientCreate, ClientUpdate
from app.schemas.case import CaseCreate, CaseUpdate
from app.schemas.task import TaskCreate, TaskUpdate

# Client Operations
def get_client(db: Session, client_id: int):
    return db.query(Client).filter(Client.id == client_id).first()

def get_clients(db: Session, lawyer_id: int, skip: int = 0, limit: int = 100):
    return db.query(Client).filter(Client.lawyer_id == lawyer_id).offset(skip).limit(limit).all()

def create_client(db: Session, client: ClientCreate, lawyer_id: int):
    db_client = Client(
        **client.dict(),
        lawyer_id=lawyer_id
    )
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client

def update_client(db: Session, client_id: int, client: ClientUpdate):
    db_client = get_client(db, client_id)
    if not db_client:
        return None
    
    update_data = client.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_client, key, value)
    
    db.commit()
    db.refresh(db_client)
    return db_client

# Case Operations
def get_case(db: Session, case_id: int):
    return db.query(Case).filter(Case.id == case_id).first()

def get_cases(db: Session, lawyer_id: int, skip: int = 0, limit: int = 100):
    return db.query(Case).filter(Case.lawyer_id == lawyer_id).offset(skip).limit(limit).all()

def create_case(db: Session, case: CaseCreate, lawyer_id: int):
    db_case = Case(
        **case.dict(),
        lawyer_id=lawyer_id
    )
    db.add(db_case)
    db.commit()
    db.refresh(db_case)
    return db_case



# Task Operations
def get_task(db: Session, task_id: int):
    return db.query(Task).filter(Task.id == task_id).first()

def get_tasks(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    """Retrieve tasks assigned to a specific user."""
    return db.query(Task).filter(Task.assigned_to == user_id).offset(skip).limit(limit).all()

def create_task(db: Session, task: TaskCreate, assigned_to: int):
    db_task = Task(
        **task.dict(),
        assigned_to=assigned_to
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def update_task(db: Session, task_id: int, task: TaskUpdate):
    db_task = get_task(db, task_id)
    if not db_task:
        return None
    
    update_data = task.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_task, key, value)
    
    db.commit()
    db.refresh(db_task)
    return db_task
