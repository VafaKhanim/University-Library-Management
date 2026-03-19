from sqlalchemy import Column, Integer, Boolean, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.base import Base, TimestampMixin


class BorrowRecord(Base, TimestampMixin):
    __tablename__ = "borrow_records"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    borrow_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    due_date = Column(DateTime, nullable=False)
    return_date = Column(DateTime, nullable=True)  # Qaytarıldıqda doldurulur
    returned = Column(Boolean, default=False)
    fine_amount = Column(Float, default=0.0)  # Cərimə məbləği

    user = relationship("User", back_populates="borrow_records")
    book = relationship("Book", back_populates="borrow_records")

    @property
    def is_overdue(self):
        """Gecikibmi?"""
        if self.returned:
            return False
        return datetime.utcnow() > self.due_date

    @property
    def days_overdue(self):
        """Neçə gün gecikib?"""
        if not self.is_overdue:
            return 0
        delta = datetime.utcnow() - self.due_date
        return delta.days

    def __repr__(self):
        return f"<BorrowRecord user={self.user_id} book={self.book_id} returned={self.returned}>"