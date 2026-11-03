"""
Exam model.
"""

import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base


class Exam(Base):
    __tablename__ = "exams"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    exam_code = Column(String, unique=True, nullable=False, index=True)
    exam_name = Column(String, nullable=False)
    total_students = Column(Integer, nullable=False)
    number_of_halls = Column(Integer, nullable=False)
    students_per_hall = Column(Integer, nullable=False)
    bench_rows = Column(Integer, nullable=True)
    bench_columns = Column(Integer, nullable=True)
    status = Column(String, nullable=False, default="draft")  # "draft" | "published"
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    creator = relationship("User", back_populates="exams")
    halls = relationship("Hall", back_populates="exam", cascade="all, delete-orphan")
    subjects = relationship("Subject", back_populates="exam", cascade="all, delete-orphan")
    seat_allocations = relationship("SeatAllocation", back_populates="exam", cascade="all, delete-orphan")
    exam_departments = relationship("ExamDepartment", back_populates="exam", cascade="all, delete-orphan")
