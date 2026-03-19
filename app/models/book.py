from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from app.models.base import Base, TimestampMixin


class Book(Base, TimestampMixin):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(20), unique=True, index=True, nullable=False)
    title = Column(String(200), nullable=False)
    author = Column(String(100), nullable=False)
    genre = Column(String(50), nullable=False)
    total_copies = Column(Integer, nullable=False, default=1)
    available_copies = Column(Integer, nullable=False, default=1)
    description = Column(String(500), nullable=True)

    borrow_records = relationship("BorrowRecord", back_populates="book")
    reservations = relationship(
        "Reservation",
        back_populates="book",
        order_by="Reservation.created_at"
    )

    @property
    def is_available(self):
        return self.available_copies > 0

    def decrease_available(self):
        if not self.is_available:
            raise ValueError(f"'{self.title}' kitabının mövcud nüsxəsi yoxdur")
        self.available_copies -= 1

    def increase_available(self):
        if self.available_copies >= self.total_copies:
            raise ValueError(f"'{self.title}' artıq maksimum nüsxə sayına çatıb")
        self.available_copies += 1

    def __repr__(self):
        return f"<Book '{self.title}' by {self.author} ({self.available_copies}/{self.total_copies})>"