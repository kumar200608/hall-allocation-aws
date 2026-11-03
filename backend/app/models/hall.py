"""
Hall model.
"""

import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base


class Hall(Base):
    __tablename__ = "halls"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    exam_id = Column(UUID(as_uuid=True), ForeignKey("exams.id", ondelete="CASCADE"), nullable=False)
    hall_name = Column(String, nullable=False)
    capacity = Column(Integer, nullable=False)
    location_link = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    # Relationships
    exam = relationship("Exam", back_populates="halls")
    seat_allocations = relationship("SeatAllocation", back_populates="hall", cascade="all, delete-orphan")
