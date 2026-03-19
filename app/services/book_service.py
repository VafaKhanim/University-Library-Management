from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.book import Book
from app.schemas.book import BookCreate, BookUpdate


class BookService:
    def __init__(self, db: Session):
        self._db = db

    def create_book(self, data: BookCreate) -> Book:
        existing = self._db.query(Book).filter(Book.code == data.code.upper()).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Bu kodlu kitab artıq mövcuddur: {data.code}"
            )

        book = Book(
            code=data.code.upper(),
            title=data.title,
            author=data.author,
            genre=data.genre,
            total_copies=data.total_copies,
            available_copies=data.total_copies,
            description=data.description
        )

        self._db.add(book)
        self._db.commit()
        self._db.refresh(book)
        return book

    def get_all_books(
        self,
        search: str = None,
        genre: str = None,
        available_only: bool = False,
        skip: int = 0,
        limit: int = 50
    ) -> tuple[list[Book], int]:

        query = self._db.query(Book)

        if search:
            query = query.filter(
                Book.title.ilike(f"%{search}%") |
                Book.author.ilike(f"%{search}%")
            )

        if genre:
            query = query.filter(Book.genre.ilike(f"%{genre}%"))

        if available_only:
            query = query.filter(Book.available_copies > 0)

        total = query.count()
        books = query.offset(skip).limit(limit).all()
        return books, total

    def get_book_by_id(self, book_id: int) -> Book:
        book = self._db.query(Book).filter(Book.id == book_id).first()
        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Kitab tapılmadı: ID {book_id}"
            )
        return book

    def update_book(self, book_id: int, data: BookUpdate) -> Book:
        book = self.get_book_by_id(book_id)

        if data.title is not None:
            book.title = data.title
        if data.author is not None:
            book.author = data.author
        if data.genre is not None:
            book.genre = data.genre
        if data.description is not None:
            book.description = data.description
        if data.total_copies is not None:
            diff = data.total_copies - book.total_copies
            book.total_copies = data.total_copies
            book.available_copies = max(0, book.available_copies + diff)

        self._db.commit()
        self._db.refresh(book)
        return book

    def delete_book(self, book_id: int):
        book = self.get_book_by_id(book_id)

        if not book.is_available:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Kitabın aktiv götürmüsü var, əvvəlcə qaytarılmalıdır"
            )

        self._db.delete(book)
        self._db.commit()