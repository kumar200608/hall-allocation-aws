"""
Pydantic schemas for Exam CRUD operations.
"""

from pydantic import BaseModel
from datetime import datetime


# ── Subject ──────────────────────────────────────────────────────────────────

class SubjectCreate(BaseModel):
    subject_name: str
    subject_code: str | None = None
    use_shared_seating: bool = False


class SubjectResponse(BaseModel):
    id: str
    exam_id: str
    subject_name: str
    subject_code: str | None
    use_shared_seating: bool
    created_at: datetime

    class Config:
        from_attributes = True


# ── Hall ─────────────────────────────────────────────────────────────────────

class HallCreate(BaseModel):
    hall_name: str
    capacity: int
    location_link: str | None = None


class HallResponse(BaseModel):
    id: str
    exam_id: str
    hall_name: str
    capacity: int
    location_link: str | None
    created_at: datetime

    class Config:
        from_attributes = True


# ── Department ───────────────────────────────────────────────────────────────

class DepartmentCreate(BaseModel):
    name: str


class DepartmentResponse(BaseModel):
    id: str
    name: str

    class Config:
        from_attributes = True


# ── Student (for CSV upload payload) ─────────────────────────────────────────

class StudentData(BaseModel):
    name: str
    registration_number: str
    department: str


# ── Department with students (for exam creation) ────────────────────────────

class DepartmentWithStudents(BaseModel):
    name: str
    students: list[StudentData]


# ── Exam ─────────────────────────────────────────────────────────────────────

class ExamCreate(BaseModel):
    exam_name: str
    exam_code: str
    bench_rows: int
    bench_columns: int
    use_shared_seating: bool = True
    shuffle_classes: bool = True
    subjects: list[SubjectCreate]
    halls: list[HallCreate]
    departments: list[DepartmentWithStudents]


class ExamUpdate(BaseModel):
    exam_name: str | None = None
    exam_code: str | None = None
    bench_rows: int | None = None
    bench_columns: int | None = None
    use_shared_seating: bool | None = None
    shuffle_classes: bool | None = None
    subjects: list[SubjectCreate] | None = None
    halls: list[HallCreate] | None = None
    departments: list[DepartmentWithStudents] | None = None


class ExamResponse(BaseModel):
    id: str
    exam_code: str
    exam_name: str
    total_students: int
    number_of_halls: int
    students_per_hall: int
    bench_rows: int | None
    bench_columns: int | None
    status: str
    created_by: str | None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ExamDetailResponse(ExamResponse):
    halls: list[HallResponse]
    subjects: list[SubjectResponse]


# ── Seat Allocation ──────────────────────────────────────────────────────────

class SeatAllocationResponse(BaseModel):
    id: str
    exam_id: str
    hall_id: str
    subject_id: str | None
    department_name: str | None
    student_name: str
    registration_number: str
    seat_number: int
    row_number: int | None
    column_number: int | None

    class Config:
        from_attributes = True


class StudentSeatLookup(BaseModel):
    exam_code: str
    registration_number: str


class StudentSeatResult(BaseModel):
    student: SeatAllocationResponse
    hall: HallResponse
    exam: ExamResponse
    all_seats: list[SeatAllocationResponse]
