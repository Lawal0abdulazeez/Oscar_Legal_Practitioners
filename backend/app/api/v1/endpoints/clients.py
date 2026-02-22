from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api import deps
from app.services import crm_service
from app.schemas.client import Client, ClientCreate, ClientUpdate
from app.models.user import User

router = APIRouter()

@router.get("/", response_model=List[Client])
def read_clients(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve clients.
    """
    clients = crm_service.get_clients(db, lawyer_id=current_user.id, skip=skip, limit=limit)
    return clients

@router.post("/", response_model=Client, status_code=status.HTTP_201_CREATED)
def create_client(
    *,
    db: Session = Depends(deps.get_db),
    client_in: ClientCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new client.
    """
    client = crm_service.create_client(db, client=client_in, lawyer_id=current_user.id)
    return client

@router.get("/{id}", response_model=Client)
def read_client(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get client by ID.
    """
    client = crm_service.get_client(db, client_id=id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    if client.lawyer_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return client

@router.put("/{id}", response_model=Client)
def update_client(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    client_in: ClientUpdate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a client.
    """
    client = crm_service.get_client(db, client_id=id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    if client.lawyer_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    client = crm_service.update_client(db, client_id=id, client=client_in)
    return client
