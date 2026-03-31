from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.core.database import get_db
from app.core.dependencies import get_current_admin
from app.schemas.user import UserCreate, UserUpdate, UserResponse, UserListResponse
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserResponse, status_code=201)
def create_user(
    data: UserCreate,
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin)
):
    service = UserService(db)
    user = service.create_user(data)
    response = UserResponse(
        id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        role=user.role.value,
        is_active=user.is_active,
        borrow_limit=user.get_borrow_limit(),
        borrow_duration=user.get_borrow_duration(),
        created_at=user.created_at
    )
    return response


@router.get("/", response_model=UserListResponse)
def get_all_users(
    role = Query(None, description="student və ya teacher"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin)
):
    service = UserService(db)
    users, total = service.get_all_users(role=role, skip=skip, limit=limit)
    user_responses = [
        UserResponse(
            id=u.id,
            first_name=u.first_name,
            last_name=u.last_name,
            email=u.email,
            role=u.role.value,
            is_active=u.is_active,
            borrow_limit=u.get_borrow_limit(),
            borrow_duration=u.get_borrow_duration(),
            created_at=u.created_at
        ) for u in users
    ]
    return UserListResponse(total=total, users=user_responses)


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id,
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin)
):
    service = UserService(db)
    user = service.get_user_by_id(user_id)
    return UserResponse(
        id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        role=user.role.value,
        is_active=user.is_active,
        borrow_limit=user.get_borrow_limit(),
        borrow_duration=user.get_borrow_duration(),
        created_at=user.created_at
    )


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id,
    data: UserUpdate,
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin)
):
    service = UserService(db)
    user = service.update_user(user_id, data)
    return UserResponse(
        id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        role=user.role.value,
        is_active=user.is_active,
        borrow_limit=user.get_borrow_limit(),
        borrow_duration=user.get_borrow_duration(),
        created_at=user.created_at
    )


@router.delete("/{user_id}", status_code=204)
def delete_user(
    user_id,
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin)
):
    service = UserService(db)
    service.delete_user(user_id)