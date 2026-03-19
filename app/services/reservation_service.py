from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.reservation import Reservation
from app.models.book import Book
from app.models.user import User
from app.notifications.base import NotificationContext
from app.notifications.email_notification import EmailNotification


class ReservationQueue:
    """
    Observer Pattern istifade olunub burda - kitab mövcud olanda növbədəkilərə xəbər vermek üçündür.
    """

    def __init__(self, db: Session):
        self._db = db
        self._notifier = NotificationContext(EmailNotification())

    def add_user(self, user: User, book: Book) -> Reservation:
        existing = self._db.query(Reservation).filter(
            Reservation.user_id == user.id,
            Reservation.book_id == book.id,
            Reservation.is_active == True
        ).first()

        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Bu istifadəçi artıq növbədədir"
            )

        reservation = Reservation(
            user_id=user.id,
            book_id=book.id,
            is_active=True
        )

        self._db.add(reservation)
        self._db.commit()
        self._db.refresh(reservation)
        return reservation

    def remove_user(self, user_id: int, book_id: int):
        reservation = self._db.query(Reservation).filter(
            Reservation.user_id == user_id,
            Reservation.book_id == book_id,
            Reservation.is_active == True
        ).first()

        if reservation:
            reservation.is_active = False
            self._db.commit()

    def get_next_user(self, book_id: int):
        reservation = self._db.query(Reservation).filter(
            Reservation.book_id == book_id,
            Reservation.is_active == True
        ).order_by(Reservation.created_at).first()

        return reservation

    def notify_next_user(self, book: Book):
        next_reservation = self.get_next_user(book.id)

        if next_reservation and next_reservation.user:
            user = next_reservation.user
            self._notifier.notify(
                recipient=user.email,
                subject="Kitab mövcuddur!",
                message=f"Hörmətli {user.full_name}, rezerv etdiyiniz '{book.title}' kitabı artıq mövcuddur."
            )

            self.remove_user(next_reservation.user_id, next_reservation.book_id)


class ReservationService:

    def __init__(self, db: Session):
        self._db = db
        self._queue = ReservationQueue(db)

    def reserve_book(self, user_id: int, book_id: int) -> Reservation:
        user = self._db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="İstifadəçi tapılmadı")

        book = self._db.query(Book).filter(Book.id == book_id).first()
        if not book:
            raise HTTPException(status_code=404, detail="Kitab tapılmadı")

        if book.is_available:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Kitab mövcuddur, birbaşa götürə bilərsiniz"
            )

        return self._queue.add_user(user, book)

    def cancel_reservation(self, user_id: int, book_id: int):
        self._queue.remove_user(user_id, book_id)

    def get_book_reservations(self, book_id: int) -> list[Reservation]:
        return self._db.query(Reservation).filter(
            Reservation.book_id == book_id,
            Reservation.is_active == True
        ).order_by(Reservation.created_at).all()