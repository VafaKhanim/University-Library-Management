from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.core.database import engine, SessionLocal
from app.core.config import settings
from app.models.base import Base

from app.models.user import User, AdminUser, UserRole
from app.models.book import Book
from app.models.borrow_record import BorrowRecord
from app.models.reservation import Reservation

from app.routers import auth, users, books, borrow, reservation, stats


def create_tables():
    Base.metadata.create_all(bind=engine)


def create_first_admin():
    """
    Sistem ilk dəfə işə düşəndə avtomatik admin yaradılması üçün configdi bu.
    Singleton pattern mentiqi ilə işləyir bu.
    """
    from app.services.auth_service import AuthService
    db: Session = SessionLocal()
    try:
        service = AuthService(db)
        service.create_first_admin(
            username=settings.FIRST_ADMIN_USERNAME,
            password=settings.FIRST_ADMIN_PASSWORD,
            full_name="Baş Administrator"
        )
        print(f"✅ Admin hazırdır: {settings.FIRST_ADMIN_USERNAME}")
    finally:
        db.close()


app = FastAPI(
    title="University Library Management System",
    description="""
    Universitet Kitabxana İdarəetmə Sistemi

    Bu sistem kitabxana işçiləri üçün nəzərdə tutulmuşdur.

    İmkanlar:
    - 📚 Kitab idarəetməsi
    - 👥 İstifadəçi idarəetməsi (tələbə/müəllim)
    - 📖 Kitab vermə və qəbul etmə
    - 🔖 Rezervasiya sistemi (FIFO növbə)
    - 📊 Statistika və hesabatlar
    - ⚠️ Gecikmiş kitablar və cərimə sistemi
    """,
    version="1.0.0",
)

# CORS - frontend üçün gelecekde düzeldile biler
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(books.router)
app.include_router(borrow.router)
app.include_router(reservation.router)
app.include_router(stats.router)


@app.on_event("startup")
def startup_event():
    """Server işə düşəndə avtomatik işləyir"""
    print("🚀 Server işə düşür...")
    create_tables()
    print("✅ Cədvəllər hazırdır")
    create_first_admin()
    print("🎉 Sistem hazırdır!")


@app.get("/", tags=["Root"])
def root():
    return {
        "message": "University Library Management System",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "active"
    }


@app.get("/health", tags=["Root"])
def health_check():
    return {"status": "healthy"}