"""
SeatAllocation model.
"""

import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base


class SeatAllocation(Base):
    __tablename__ = "seat_allocations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    exam_id = Column(UUID(as_uuid=True), ForeignKey("exams.id", ondelete="CASCADE"), nullable=False)
    hall_id = Column(UUID(as_uuid=True), ForeignKey("halls.id", ondelete="CASCADE"), nullable=False)
    subject_id = Column(UUID(as_uuid=True), ForeignKey("subjects.id", ondelete="CASCADE"), nullable=True)
    department_name = Column(String, nullable=True)
    student_name = Column(String, nullable=False)
    registration_number = Column(String, nullable=False)
    seat_number = Column(Integer, nullable=False)
    row_number = Column(Integer, nullable=True)
    column_number = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    # Relationships
    exam = relationship("Exam", back_populates="seat_allocations")
    hall = relationship("Hall", back_populates="seat_allocations")
    subject = relationship("Subject", back_populates="seat_allocations")
