from app.models.borrow_record import BorrowRecord

FINE_PER_DAY = 0.50 #cerime deyerini sonra burdan deyismek olar

class FineService:

    @staticmethod
    def calculate_fine(record: BorrowRecord) -> float:
        if not record.is_overdue:
            return 0.0
        return round(record.days_overdue * FINE_PER_DAY, 2)

    @staticmethod
    def apply_fine(record: BorrowRecord) -> float:
        fine = FineService.calculate_fine(record)
        record.fine_amount = fine
        return fine