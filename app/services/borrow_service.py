from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.borrow_record import BorrowRecord
from app.models.book import Book
from app.models.user import User
from app.services.fine_service import FineService
from app.services.reservation_service import ReservationQueue


class BorrowService:
    def __init__(self, db: Session):
        self._db = db
        self._fine_service = FineService()
        self._queue = ReservationQueue(db)

    def borrow_book(self, user_id: int, book_id: int) -> BorrowRecord:
        user = self._db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="İstifadəçi tapılmadı")

        book = self._db.query(Book).filter(Book.id == book_id).first()
        if not book:
            raise HTTPException(status_code=404, detail="Kitab tapılmadı")

        if not book.is_available:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"'{book.title}' kitabının mövcud nüsxəsi yoxdur"
            )

        if not user.can_borrow():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Limit dolub: maksimum {user.get_borrow_limit()} kitab götürə bilərsiniz"
            )

        already = self._db.query(BorrowRecord).filter(
            BorrowRecord.user_id == user_id,
            BorrowRecord.book_id == book_id,
            BorrowRecord.returned == False
        ).first()
        if already:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Bu kitab artıq bu istifadəçidədir"
            )

        book.decrease_available()

        due_date = datetime.utcnow()
        from datetime import timedelta
        due_date = datetime.utcnow() + timedelta(days=user.get_borrow_duration())

        record = BorrowRecord(
            user_id=user_id,
            book_id=book_id,
            due_date=due_date
        )

        self._db.add(record)
        self._db.commit()
        self._db.refresh(record)
        return record

    def return_book(self, user_id: int, book_id: int) -> BorrowRecord:
        record = self._db.query(BorrowRecord).filter(
            BorrowRecord.user_id == user_id,
            BorrowRecord.book_id == book_id,
            BorrowRecord.returned == False
        ).first()

        if not record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Aktiv götürmə qeydi tapılmadı"
            )

        book = record.book

        self._fine_service.apply_fine(record)

        record.returned = True
        record.return_date = datetime.utcnow()

        book.increase_available()

        self._db.commit()
        self._db.refresh(record)

        # Observer Pattern — növbədəki istifadəçiyə xəbər vermək üçün
        self._queue.notify_next_user(book)

        return record

    def get_active_borrows(self, skip: int = 0, limit: int = 50):
        query = self._db.query(BorrowRecord).filter(BorrowRecord.returned == False)
        total = query.count()
        records = query.offset(skip).limit(limit).all()
        return records, total

    def get_overdue_borrows(self) -> list[BorrowRecord]:
        all_active = self._db.query(BorrowRecord).filter(
            BorrowRecord.returned == False
        ).all()
        result = []
        for r in all_active:
            if r.is_overdue:
                result.append(r)
        return result

    def get_user_borrow_history(self, user_id: int) -> list[BorrowRecord]:
        return self._db.query(BorrowRecord).filter(
            BorrowRecord.user_id == user_id
        ).order_by(BorrowRecord.borrow_date.desc()).all()