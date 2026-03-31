from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.core.database import get_db
from app.core.dependencies import get_current_admin
from app.schemas.book import BookCreate, BookUpdate, BookResponse, BookListResponse
from app.services.book_service import BookService

router = APIRouter(prefix="/books", tags=["Books"])


@router.post("/", response_model=BookResponse, status_code=201)
def create_book(
    data: BookCreate,
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin)
):
    service = BookService(db)
    return service.create_book(data)


@router.get("/", response_model=BookListResponse)
def get_all_books(
    search = Query(None, description="Ad və ya müəllifə görə axtar"),
    genre = Query(None, description="Janra görə filter"),
    available_only = Query(False, description="Yalnız mövcud kitablar"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin)
):
    service = BookService(db)
    books, total = service.get_all_books(
        search=search,
        genre=genre,
        available_only=available_only,
        skip=skip,
        limit=limit
    )
    return BookListResponse(total=total, books=books)


@router.get("/{book_id}", response_model=BookResponse)
def get_book(
    book_id,
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin)
):
    service = BookService(db)
    return service.get_book_by_id(book_id)


@router.put("/{book_id}", response_model=BookResponse)
def update_book(
    book_id,
    data: BookUpdate,
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin)
):
    service = BookService(db)
    return service.update_book(book_id, data)


@router.delete("/{book_id}", status_code=204)
def delete_book(
    book_id,
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin)
):
    service = BookService(db)
    service.delete_book(book_id)