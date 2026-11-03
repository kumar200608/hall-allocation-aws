"""
Smart seat allocation algorithm replicating the matrix logic.
Supports pairwise department interleaving (shuffle) and grid seating.
"""

from typing import Any
import re


def natural_sort_key(s: str) -> list[Any]:
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r"(\d+)", s)]


def get_ordered_students(departments: list[dict], should_shuffle: bool) -> list[dict]:
    """
    If should_shuffle is False or number of departments is odd,
    return sequential student list.
    Otherwise, interleave pairwise (depts[0]&[1], [2]&[3], etc.).
    """
    if not should_shuffle or len(departments) % 2 != 0:
        flat = []
        for d in departments:
            flat.extend(list(d["students"]))
        return flat

    result = []
    for i in range(0, len(departments), 2):
        pair = departments[i : i + 2]
        queues = [list(d["students"]) for d in pair]
        active = True
        while active:
            active = False
            for q in queues:
                if q:
                    result.append(q.pop(0))
                    active = True
    return result


def allocate_seats_for_hall(
    students_queue: list[dict],
    rows: int,
    cols: int,
    hall_id: Any,
    subject_id: Any = None,
) -> list[dict]:
    allocations = []
    for row in range(1, rows + 1):
        for col in range(1, cols + 1):
            if not students_queue:
                return allocations
            student = students_queue.pop(0)
            allocations.append({
                "hall_id": hall_id,
                "student_name": student["name"],
                "registration_number": student["registration_number"],
                "department_name": student.get("department"),
                "seat_number": len(allocations) + 1,
                "row_number": row,
                "column_number": col,
                "subject_id": subject_id,
            })
    return allocations
