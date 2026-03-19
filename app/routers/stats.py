from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.database import get_db
from app.core.dependencies import get_current_admin
from app.models.user import User, UserRole
from app.models.book import Book
from app.models.borrow_record import BorrowRecord
from app.models.reservation import Reservation
from app.services.borrow_service import BorrowService

router = APIRouter(prefix="/stats", tags=["Statistics"])


@router.get("/")
def get_statistics(
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin)
):
    """Admin dashboard üçün ümumi statistika"""
    borrow_service = BorrowService(db)

    total_books = db.query(Book).count()
    total_users = db.query(User).count()
    total_students = db.query(User).filter(User.role == UserRole.STUDENT).count()
    total_teachers = db.query(User).filter(User.role == UserRole.TEACHER).count()
    active_borrows = db.query(BorrowRecord).filter(BorrowRecord.returned == False).count()
    total_borrows = db.query(BorrowRecord).count()
    active_reservations = db.query(Reservation).filter(Reservation.is_active == True).count()
    overdue_count = len(borrow_service.get_overdue_borrows())

    # Ən çox götürülən 5 kitab
    top_books = db.query(
        Book.title,
        Book.author,
        func.count(BorrowRecord.id).label("borrow_count")
    ).join(BorrowRecord).group_by(Book.id).order_by(
        func.count(BorrowRecord.id).desc()
    ).limit(5).all()

    return {
        "books": {
            "total": total_books,
        },
        "users": {
            "total": total_users,
            "students": total_students,
            "teachers": total_teachers,
        },
        "borrows": {
            "active": active_borrows,
            "total": total_borrows,
            "overdue": overdue_count,
        },
        "reservations": {
            "active": active_reservations,
        },
        "top_books": [
            {
                "title": b.title,
                "author": b.author,
                "borrow_count": b.borrow_count
            } for b in top_books
        ]
    }