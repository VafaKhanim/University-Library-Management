from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.schemas.user import UserResponse
from app.schemas.book import BookResponse


class ReservationCreate(BaseModel):
    user_id: int
    book_id: int


class ReservationResponse(BaseModel):
    id: int
    user: UserResponse
    book: BookResponse
    is_active: bool
    created_at: datetime
    queue_position: Optional[int] = None  # Növbədə neçənci

    model_config = {"from_attributes": True}


class ReservationListResponse(BaseModel):
    total: int
    reservations: list[ReservationResponse]