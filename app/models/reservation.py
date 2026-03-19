from sqlalchemy import Column, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.models.base import Base, TimestampMixin


class Reservation(Base, TimestampMixin):
    """
    Rezervasiya modeli — FIFO növbəsi.
    """
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    is_active = Column(Boolean, default=True)  # False = ləğv edilib və ya tamamlanıb

    user = relationship("User", back_populates="reservations")
    book = relationship("Book", back_populates="reservations")

    def __repr__(self):
        return f"<Reservation user={self.user_id} book={self.book_id} active={self.is_active}>"