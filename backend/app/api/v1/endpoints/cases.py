from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api import deps
from app.services import crm_service
from app.schemas.case import Case, CaseCreate, CaseUpdate
from app.models.user import User

router = APIRouter()

@router.get("/", response_model=List[Case])
def read_cases(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve cases.
    """
    cases = crm_service.get_cases(db, lawyer_id=current_user.id, skip=skip, limit=limit)
    return cases

@router.post("/", response_model=Case, status_code=status.HTTP_201_CREATED)
def create_case(
    *,
    db: Session = Depends(deps.get_db),
    case_in: CaseCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new case.
    """
    case = crm_service.create_case(db, case=case_in, lawyer_id=current_user.id)
    return case

@router.get("/{id}", response_model=Case)
def read_case(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get case by ID.
    """
    case = crm_service.get_case(db, case_id=id)
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    if case.lawyer_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return case

@router.put("/{id}", response_model=Case)
def update_case(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    case_in: CaseUpdate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a case.
    """
    case = crm_service.get_case(db, case_id=id)
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    if case.lawyer_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    case = crm_service.update_case(db, case_id=id, case=case_in)
    return case
