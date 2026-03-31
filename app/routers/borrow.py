from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_admin
from app.schemas.borrow import BorrowCreate, ReturnBook, BorrowRecordResponse, BorrowListResponse, OverdueListResponse
from app.services.borrow_service import BorrowService

router = APIRouter(prefix="/borrow", tags=["Borrow"])


@router.post("/", response_model=BorrowRecordResponse, status_code=201)
def borrow_book(
    data: BorrowCreate,
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin)
):
    service = BorrowService(db)
    return service.borrow_book(data.user_id, data.book_id)


@router.post("/return", response_model=BorrowRecordResponse)
def return_book(
    data: ReturnBook,
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin)
):
    service = BorrowService(db)
    return service.return_book(data.user_id, data.book_id)


@router.get("/active", response_model=BorrowListResponse)
def get_active_borrows(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin)
):
    service = BorrowService(db)
    records, total = service.get_active_borrows(skip=skip, limit=limit)
    return BorrowListResponse(total=total, records=records)


@router.get("/overdue", response_model=OverdueListResponse)
def get_overdue_borrows(
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin)
):
    service = BorrowService(db)
    records = service.get_overdue_borrows()
    return OverdueListResponse(total=len(records), records=records)


@router.get("/history/{user_id}", response_model=BorrowListResponse)
def get_user_history(
    user_id,
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin)
):
    service = BorrowService(db)
    records = service.get_user_borrow_history(user_id)
    return BorrowListResponse(total=len(records), records=records)