from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from app.models.case import CaseStatus, CasePriority

class CaseBase(BaseModel):
    client_id: int
    case_number: str
    title: str
    description: Optional[str] = None
    status: CaseStatus = CaseStatus.OPEN
    priority: CasePriority = CasePriority.MEDIUM

class CaseCreate(CaseBase):
    pass

class CaseUpdate(CaseBase):
    client_id: Optional[int] = None
    case_number: Optional[str] = None
    title: Optional[str] = None
    status: Optional[CaseStatus] = None
    priority: Optional[CasePriority] = None

class CaseInDBBase(CaseBase):
    id: int
    lawyer_id: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    closed_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class Case(CaseInDBBase):
    pass
