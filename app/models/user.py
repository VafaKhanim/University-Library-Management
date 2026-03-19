from abc import ABC, abstractmethod
from sqlalchemy import Column, String, Integer, Boolean, Enum
from sqlalchemy.orm import relationship
import enum
from app.models.base import Base, TimestampMixin


class UserRole(enum.Enum):
    STUDENT = "student"
    TEACHER = "teacher"


# Abstract base classdı bu
class LibraryUser(ABC):
    @abstractmethod
    def get_borrow_limit(self) -> int:
        """Neçə kitab götürə bilər — implement edilir diger classlar terefinden (Polymorphism)"""
        pass

    @abstractmethod
    def get_borrow_duration(self) -> int:
        """bu da eyni şekilde - burda max neçə günlük kitab götürülə bilərdi"""
        pass


# INHERITANCE burda olur
class Student(LibraryUser):
    def get_borrow_limit(self) -> int:
        return 3
    def get_borrow_duration(self) -> int:
        return 14


class Teacher(LibraryUser):
    def get_borrow_limit(self) -> int:
        return 5
    def get_borrow_duration(self) -> int:
        return 30



# DB Model
class User(Base, TimestampMixin):

    #Encapsulation nümunəsidir bu -- _role, _borrowed_count private atributlar kimi

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    is_active = Column(Boolean, default=True)

    borrow_records = relationship("BorrowRecord", back_populates="user", lazy="dynamic")
    reservations = relationship("Reservation", back_populates="user", lazy="dynamic")

    # Encapsulation — private atributlar burda işlənib
    @property
    def _borrowed_count(self) -> int:
        return self.borrow_records.filter_by(returned=False).count()

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def get_library_user(self) -> LibraryUser:
        """
        Factory method işlənib — role-a görə doğru OOP obyektini qaytarır.
        Polymorphism burda işlənir.
        """
        if self.role == UserRole.STUDENT:
            return Student()
        return Teacher()

    def get_borrow_limit(self) -> int:
        return self.get_library_user().get_borrow_limit()

    def get_borrow_duration(self) -> int:
        return self.get_library_user().get_borrow_duration()

    def can_borrow(self) -> bool:
        return self._borrowed_count < self.get_borrow_limit()

    def __repr__(self):
        return f"<User {self.full_name} ({self.role.value})>"



# Admin Model — kitabxana işçisi
class AdminUser(Base, TimestampMixin):
    __tablename__ = "admin_users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=True)

    def __repr__(self):
        return f"<AdminUser {self.username}>"