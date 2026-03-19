from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional

# REQUEST schemas
class BookCreate(BaseModel):
    code: str
    title: str
    author: str
    genre: str
    total_copies: int = 1
    description: Optional[str] = None

    @field_validator("total_copies")
    @classmethod
    def copies_must_be_positive(cls, v):
        if v < 1:
            raise ValueError("Nüsxə sayı ən azı 1 olmalıdır")
        return v

    @field_validator("code")
    @classmethod
    def code_must_be_uppercase(cls, v):
        return v.upper()


class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    genre: Optional[str] = None
    total_copies: Optional[int] = None
    description: Optional[str] = None



# RESPONSE schemas
class BookResponse(BaseModel):
    id: int
    code: str
    title: str
    author: str
    genre: str
    total_copies: int
    available_copies: int
    description: Optional[str]
    is_available: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class BookListResponse(BaseModel):
    total: int
    books: list[BookResponse]