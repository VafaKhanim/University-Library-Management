from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_admin
from app.schemas.reservation import ReservationCreate, ReservationResponse, ReservationListResponse
from app.services.reservation_service import ReservationService

router = APIRouter(prefix="/reservations", tags=["Reservations"])


@router.post("/", response_model=ReservationResponse, status_code=201)
def reserve_book(
        data: ReservationCreate,
        db: Session = Depends(get_db),
        admin = Depends(get_current_admin)
):
    service = ReservationService(db)
    reservation = service.reserve_book(data.user_id, data.book_id)

    # Növbə pozisiyasını hesablayir
    all_reservations = service.get_book_reservations(data.book_id)

    position = None
    for i, r in enumerate(all_reservations):
        if r.id == reservation.id:
            position = i + 1
            break

    response = ReservationResponse(
        id=reservation.id,
        user=reservation.user,
        book=reservation.book,
        is_active=reservation.is_active,
        created_at=reservation.created_at,
        queue_position=position
    )
    return response


@router.delete("/{user_id}/{book_id}", status_code=204)
def cancel_reservation(
        user_id,
        book_id,
        db: Session = Depends(get_db),
        admin = Depends(get_current_admin)
):
    service = ReservationService(db)
    service.cancel_reservation(user_id, book_id)


@router.get("/book/{book_id}", response_model=ReservationListResponse)
def get_book_reservations(
        book_id,
        db: Session = Depends(get_db),
        admin = Depends(get_current_admin)
):
    service = ReservationService(db)
    reservations = service.get_book_reservations(book_id)
    return ReservationListResponse(total=len(reservations), reservations=reservations)