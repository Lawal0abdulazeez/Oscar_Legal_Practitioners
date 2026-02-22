from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime
from app.models.client import ClientStatus

class ClientBase(BaseModel):
    name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    status: ClientStatus = ClientStatus.ACTIVE
    notes: Optional[str] = None

class ClientCreate(ClientBase):
    pass

class ClientUpdate(ClientBase):
    name: Optional[str] = None
    status: Optional[ClientStatus] = None

class ClientInDBBase(ClientBase):
    id: int
    lawyer_id: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class Client(ClientInDBBase):
    pass
