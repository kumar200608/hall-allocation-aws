"""
Student search & lookup routes.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.exam import Exam
from app.models.hall import Hall
from app.models.seat_allocation import SeatAllocation
from app.schemas.exam import StudentSeatResult

router = APIRouter(prefix="/students", tags=["Students"])


@router.get("/lookup", response_model=StudentSeatResult)
def lookup_student_seat(
    exam_code: str = Query(..., description="The unique exam code e.g. EXM1025"),
    registration_number: str = Query(..., description="Student roll or registration number"),
    db: Session = Depends(get_db),
):
    """
    Search for a student's assigned exam seat, hall info, and adjacent hall layout.
    """
    exam = db.query(Exam).filter(Exam.exam_code == exam_code.strip()).first()
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found with provided exam code")

    clean_reg = registration_number.strip().replace(" ", "")
    seat = (
        db.query(SeatAllocation)
        .filter(
            SeatAllocation.exam_id == exam.id,
            SeatAllocation.registration_number == clean_reg,
        )
        .first()
    )

    if not seat:
        raise HTTPException(
            status_code=404,
            detail=f"No seating record found for registration number '{registration_number}' in exam '{exam_code}'",
        )

    hall = db.query(Hall).filter(Hall.id == seat.hall_id).first()
    if not hall:
        raise HTTPException(status_code=404, detail="Assigned hall not found")

    all_seats = (
        db.query(SeatAllocation)
        .filter(SeatAllocation.hall_id == hall.id)
        .order_by(SeatAllocation.seat_number.asc())
        .all()
    )

    return {
        "student": seat,
        "hall": hall,
        "exam": exam,
        "all_seats": all_seats,
    }
