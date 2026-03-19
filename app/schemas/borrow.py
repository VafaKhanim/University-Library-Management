from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class UserInBorrow(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    role: str

    model_config = {"from_attributes": True}


class BookInBorrow(BaseModel):
    id: int
    code: str
    title: str
    author: str
    genre: str
    available_copies: int
    total_copies: int

    model_config = {"from_attributes": True}


class BorrowCreate(BaseModel):
    user_id: int
    book_id: int


class ReturnBook(BaseModel):
    user_id: int
    book_id: int


class BorrowRecordResponse(BaseModel):
    id: int
    user: UserInBorrow
    book: BookInBorrow
    borrow_date: datetime
    due_date: datetime
    return_date: Optional[datetime]
    returned: bool
    is_overdue: bool
    days_overdue: int
    fine_amount: float

    model_config = {"from_attributes": True}


class BorrowListResponse(BaseModel):
    total: int
    records: list[BorrowRecordResponse]


class OverdueListResponse(BaseModel):
    total: int
    records: list[BorrowRecordResponse]