"""Initial schema migration

Revision ID: 001_initial_schema
Revises:
Create Date: 2026-11-04 01:54:00

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "001_initial_schema"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. users
    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("email", sa.String(), nullable=False, unique=True, index=True),
        sa.Column("hashed_password", sa.String(), nullable=False),
        sa.Column("full_name", sa.String(), nullable=True),
        sa.Column("username", sa.String(), unique=True, nullable=True),
        sa.Column("role", sa.String(), nullable=False, server_default="student"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
    )

    # 2. exams
    op.create_table(
        "exams",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("exam_code", sa.String(), nullable=False, unique=True, index=True),
        sa.Column("exam_name", sa.String(), nullable=False),
        sa.Column("total_students", sa.Integer(), nullable=False),
        sa.Column("number_of_halls", sa.Integer(), nullable=False),
        sa.Column("students_per_hall", sa.Integer(), nullable=False),
        sa.Column("bench_rows", sa.Integer(), nullable=True),
        sa.Column("bench_columns", sa.Integer(), nullable=True),
        sa.Column("status", sa.String(), nullable=False, server_default="draft"),
        sa.Column("created_by", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
    )

    # 3. halls
    op.create_table(
        "halls",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("exam_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("exams.id", ondelete="CASCADE"), nullable=False),
        sa.Column("hall_name", sa.String(), nullable=False),
        sa.Column("capacity", sa.Integer(), nullable=False),
        sa.Column("location_link", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
    )

    # 4. subjects
    op.create_table(
        "subjects",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("exam_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("exams.id", ondelete="CASCADE"), nullable=False),
        sa.Column("subject_name", sa.String(), nullable=False),
        sa.Column("subject_code", sa.String(), nullable=True),
        sa.Column("use_shared_seating", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
    )

    # 5. departments
    op.create_table(
        "departments",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(), nullable=False, unique=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
    )

    # 6. exam_departments
    op.create_table(
        "exam_departments",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("exam_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("exams.id", ondelete="CASCADE"), nullable=False),
        sa.Column("department_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("departments.id", ondelete="CASCADE"), nullable=False),
        sa.Column("student_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
        sa.UniqueConstraint("exam_id", "department_id"),
    )

    # 7. seat_allocations
    op.create_table(
        "seat_allocations",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("exam_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("exams.id", ondelete="CASCADE"), nullable=False),
        sa.Column("hall_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("halls.id", ondelete="CASCADE"), nullable=False),
        sa.Column("subject_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("subjects.id", ondelete="CASCADE"), nullable=True),
        sa.Column("department_name", sa.String(), nullable=True),
        sa.Column("student_name", sa.String(), nullable=False),
        sa.Column("registration_number", sa.String(), nullable=False),
        sa.Column("seat_number", sa.Integer(), nullable=False),
        sa.Column("row_number", sa.Integer(), nullable=True),
        sa.Column("column_number", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
    )


def downgrade() -> None:
    op.drop_table("seat_allocations")
    op.drop_table("exam_departments")
    op.drop_table("departments")
    op.drop_table("subjects")
    op.drop_table("halls")
    op.drop_table("exams")
    op.drop_table("users")
