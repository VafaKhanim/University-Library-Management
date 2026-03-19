from pydantic import BaseModel, EmailStr
from enum import Enum
from datetime import datetime
from typing import Optional


class UserRoleSchema(str, Enum):
    STUDENT = "student"
    TEACHER = "teacher"


# REQUEST schemas
class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    role: UserRoleSchema


class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[UserRoleSchema] = None
    is_active: Optional[bool] = None



# RESPONSE schemas
class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    role: UserRoleSchema
    is_active: bool
    borrow_limit: int
    borrow_duration: int
    created_at: datetime

    model_config = {"from_attributes": True}


class UserListResponse(BaseModel):
    total: int
    users: list[UserResponse]