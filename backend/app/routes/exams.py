"""
Exam management routes (CRUD, allocation execution, details).
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import uuid
import re

from app.database import get_db
from app.models.exam import Exam
from app.models.hall import Hall
from app.models.subject import Subject
from app.models.department import Department
from app.models.exam_department import ExamDepartment
from app.models.seat_allocation import SeatAllocation
from app.models.user import User
from app.schemas.exam import (
    ExamCreate,
    ExamUpdate,
    ExamResponse,
    ExamDetailResponse,
    SeatAllocationResponse,
)
from app.auth.jwt import get_current_user, require_admin
from app.services.allocation import get_ordered_students, allocate_seats_for_hall

router = APIRouter(prefix="/exams", tags=["Exams"])


def _extract_hall_number(name: str) -> int:
    match = re.search(r"\d+", name)
    return int(match.group()) if match else 0


@router.get("", response_model=list[ExamResponse])
def list_exams(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """List all exams created by the authenticated user."""
    return (
        db.query(Exam)
        .filter(Exam.created_by == current_user.id)
        .order_by(Exam.created_at.desc())
        .all()
    )


@router.post("", response_model=ExamResponse, status_code=status.HTTP_201_CREATED)
def create_exam(
    payload: ExamCreate,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Create an exam and automatically perform smart seat allocation."""
    # Check if exam code already exists
    existing = db.query(Exam).filter(Exam.exam_code == payload.exam_code).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Exam with code '{payload.exam_code}' already exists",
        )

    # Calculate total students
    all_students_raw = []
    depts_dict_list = []
    for dept in payload.departments:
        students = [s.model_dump() for s in dept.students]
        all_students_raw.extend(students)
        depts_dict_list.append({"name": dept.name, "students": students})

    total_students = len(all_students_raw)
    students_per_hall = payload.bench_rows * payload.bench_columns
    total_capacity = students_per_hall * len(payload.halls)

    if total_students > total_capacity:
        deficit = total_students - total_capacity
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Capacity mismatch: {total_students} students but only {total_capacity} seats available. Short by {deficit} seats.",
        )

    # 1. Create Exam record
    exam = Exam(
        id=uuid.uuid4(),
        exam_code=payload.exam_code,
        exam_name=payload.exam_name,
        total_students=total_students,
        number_of_halls=len(payload.halls),
        students_per_hall=students_per_hall,
        bench_rows=payload.bench_rows,
        bench_columns=payload.bench_columns,
        status="published",
        created_by=current_user.id,
    )
    db.add(exam)
    db.flush()

    # 2. Upsert Departments & ExamDepartments
    for dept_in in payload.departments:
        dept_record = db.query(Department).filter(Department.name == dept_in.name).first()
        if not dept_record:
            dept_record = Department(id=uuid.uuid4(), name=dept_in.name)
            db.add(dept_record)
            db.flush()

        exam_dept = ExamDepartment(
            id=uuid.uuid4(),
            exam_id=exam.id,
            department_id=dept_record.id,
            student_count=len(dept_in.students),
        )
        db.add(exam_dept)

    # 3. Create Subjects
    subject_records = []
    for s in payload.subjects:
        subj = Subject(
            id=uuid.uuid4(),
            exam_id=exam.id,
            subject_name=s.subject_name,
            subject_code=s.subject_code,
            use_shared_seating=payload.use_shared_seating,
        )
        db.add(subj)
        subject_records.append(subj)
    db.flush()

    # 4. Create Halls
    hall_records = []
    for h in payload.halls:
        hall = Hall(
            id=uuid.uuid4(),
            exam_id=exam.id,
            hall_name=h.hall_name,
            capacity=h.capacity or students_per_hall,
            location_link=h.location_link,
        )
        db.add(hall)
        hall_records.append(hall)
    db.flush()

    # Sort halls numerically by name
    sorted_halls = sorted(hall_records, key=lambda x: _extract_hall_number(x.hall_name))

    # 5. Smart Seat Allocation
    allocations_to_insert = []
    if payload.use_shared_seating:
        ordered_students = get_ordered_students(depts_dict_list, payload.shuffle_classes)
        for hall in sorted_halls:
            allocated = allocate_seats_for_hall(
                ordered_students,
                payload.bench_rows,
                payload.bench_columns,
                hall.id,
            )
            for item in allocated:
                allocations_to_insert.append(
                    SeatAllocation(
                        id=uuid.uuid4(),
                        exam_id=exam.id,
                        **item,
                    )
                )
    else:
        for subj in subject_records:
            ordered_students = get_ordered_students(depts_dict_list, payload.shuffle_classes)
            for hall in sorted_halls:
                allocated = allocate_seats_for_hall(
                    ordered_students,
                    payload.bench_rows,
                    payload.bench_columns,
                    hall.id,
                    subject_id=subj.id,
                )
                for item in allocated:
                    allocations_to_insert.append(
                        SeatAllocation(
                            id=uuid.uuid4(),
                            exam_id=exam.id,
                            **item,
                        )
                    )

    db.bulk_save_objects(allocations_to_insert)
    db.commit()
    db.refresh(exam)
    return exam


@router.get("/code/{exam_code}", response_model=ExamDetailResponse)
def get_exam_by_code(exam_code: str, db: Session = Depends(get_db)):
    """Fetch public details for an exam by exam code."""
    exam = db.query(Exam).filter(Exam.exam_code == exam_code).first()
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")
    return exam


@router.get("/{exam_id}", response_model=ExamDetailResponse)
def get_exam(
    exam_id: uuid.UUID,
    db: Session = Depends(get_db),
):
    exam = db.query(Exam).filter(Exam.id == exam_id).first()
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")
    return exam


@router.get("/{exam_id}/allocations", response_model=list[SeatAllocationResponse])
def get_exam_allocations(
    exam_id: uuid.UUID,
    hall_id: uuid.UUID | None = None,
    db: Session = Depends(get_db),
):
    query = db.query(SeatAllocation).filter(SeatAllocation.exam_id == exam_id)
    if hall_id:
        query = query.filter(SeatAllocation.hall_id == hall_id)
    return query.order_by(SeatAllocation.seat_number.asc()).all()


@router.delete("/{exam_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_exam(
    exam_id: uuid.UUID,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    exam = (
        db.query(Exam)
        .filter(Exam.id == exam_id, Exam.created_by == current_user.id)
        .first()
    )
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")

    db.delete(exam)
    db.commit()
    return None
