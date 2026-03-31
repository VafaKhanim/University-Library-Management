from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user import AdminUser
from app.core.security import verify_password, create_access_token, hash_password


class AuthService:

    def __init__(self, db: Session):
        self._db = db

    def login(self, username: str, password: str) -> dict:
        admin = self._db.query(AdminUser).filter(
            AdminUser.username == username
        ).first()

        if not admin or not verify_password(password, admin.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Yanlış istifadəçi adı və ya şifrə"
            )

        if not admin.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Hesab deaktivdir"
            )

        token = create_access_token(data={"sub": admin.username})

        return {
            "access_token": token,
            "token_type": "bearer",
            "admin_name": admin.full_name
        }

    def create_first_admin(self, username: str, password: str, full_name: str):
        existing = self._db.query(AdminUser).filter(
            AdminUser.username == username
        ).first()

        if existing:
            return

        admin = AdminUser(
            username=username,
            hashed_password=hash_password(password),
            full_name=full_name
        )

        self._db.add(admin)
        self._db.commit()

    def create_admin(self, username: str, password: str, full_name: str) -> dict:
        existing = self._db.query(AdminUser).filter(
            AdminUser.username == username
        ).first()

        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Bu username artıq mövcuddur: {username}"
            )

        admin = AdminUser(
            username=username,
            hashed_password=hash_password(password),
            full_name=full_name
        )

        self._db.add(admin)
        self._db.commit()
        self._db.refresh(admin)

        token = create_access_token(data={"sub": admin.username})
        return {
            "access_token": token,
            "token_type": "bearer",
            "admin_name": admin.full_name
        }