from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core import database, security
from app.services.user_service import get_user_by_email, create_user
from app.schemas.user import UserCreate, User as UserSchema
from app.schemas.token import Token
from app.core.config import settings
from app.api import deps
from app.models.user import User

router = APIRouter()

@router.post("/register", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
def register(
    user: UserCreate,
    db: Session = Depends(database.get_db)
):
    """
    Create a new user.
    """
    existing_user = get_user_by_email(db, email=user.email)
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="User with this email already exists"
        )
    user = create_user(db=db, user=user)
    return user

@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db)
):
    """
    OAuth2 compatible token login, get an access token for future requests.
    """
    user = get_user_by_email(db, email=form_data.username)
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        subject=user.email, expires_delta=access_token_expires
    )
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.get("/me", response_model=UserSchema)
def read_users_me(
    current_user: User = Depends(deps.get_current_active_user)
):
    """
    Get current logged in user.
    """
    return current_user
