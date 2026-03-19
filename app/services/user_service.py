from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user import User, UserRole
from app.schemas.user import UserCreate, UserUpdate
from app.factories.user_factory import UserFactory


class UserService:
    def __init__(self, db: Session):
        self._db = db

    def create_user(self, data: UserCreate) -> User:
        existing = self._db.query(User).filter(User.email == data.email).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Bu email artıq qeydiyyatdadır: {data.email}"
            )

        user = UserFactory.create_user(
            first_name=data.first_name,
            last_name=data.last_name,
            email=data.email,
            role=data.role.value
        )

        self._db.add(user)
        self._db.commit()
        self._db.refresh(user)
        return user

    def get_all_users(self, role: str = None, skip: int = 0, limit: int = 50) -> tuple[list[User], int]:
        query = self._db.query(User)

        if role:
            try:
                role_enum = UserRole(role)
                query = query.filter(User.role == role_enum)
            except ValueError:
                raise HTTPException(status_code=400, detail="Yanlış rol")

        total = query.count()
        users = query.offset(skip).limit(limit).all()
        return users, total

    def get_user_by_id(self, user_id: int) -> User:
        user = self._db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"İstifadəçi tapılmadı: ID {user_id}"
            )
        return user

    def update_user(self, user_id: int, data: UserUpdate) -> User:
        user = self.get_user_by_id(user_id)

        if data.first_name is not None:
            user.first_name = data.first_name
        if data.last_name is not None:
            user.last_name = data.last_name
        if data.email is not None:
            user.email = data.email
        if data.role is not None:
            user.role = UserRole(data.role.value)
        if data.is_active is not None:
            user.is_active = data.is_active

        self._db.commit()
        self._db.refresh(user)
        return user

    def delete_user(self, user_id: int):
        user = self.get_user_by_id(user_id)
        #aktiv götürmə falan da yoxlanıla bilər
        self._db.delete(user)
        self._db.commit()