from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_admin
from app.schemas.auth import AdminLogin, TokenResponse, AdminCreate
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=TokenResponse)
def login(data: AdminLogin, db: Session = Depends(get_db)):
    service = AuthService(db)
    return service.login(data.username, data.password)


@router.post("/create-admin", response_model=TokenResponse)
def create_admin(
    data: AdminCreate,
    db: Session = Depends(get_db),
    _=Depends(get_current_admin)
):
    service = AuthService(db)
    return service.create_admin(data.username, data.password, data.full_name)