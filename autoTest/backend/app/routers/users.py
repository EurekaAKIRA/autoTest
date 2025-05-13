from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..services.user_service import UserService
from ..models.user import User, UserUpdate
from ..core.security import oauth2_scheme, verify_token

router = APIRouter()

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = verify_token(token)
    email: str = payload.get("sub")
    if email is None:
        raise credentials_exception
    
    user_service = UserService(db)
    user = user_service.get_user_by_email(email)
    if user is None:
        raise credentials_exception
    return user

@router.get("/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)) -> Any:
    return current_user

@router.get("/users", response_model=List[User])
async def read_users(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    user_service = UserService(db)
    users = user_service.get_users(skip=skip, limit=limit)
    return users

@router.put("/users/{user_id}", response_model=User)
async def update_user(
    user_id: int,
    user: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    if not current_user.is_superuser and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    user_service = UserService(db)
    return user_service.update_user(user_id, user)

@router.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    user_service = UserService(db)
    user_service.delete_user(user_id)
    return {"status": "success"} 