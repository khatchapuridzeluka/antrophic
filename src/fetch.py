"""List submissions from a local drop (AC1).

A later Classroom adapter in src/classroom.py returns the same records.
"""

import json
import re
from pathlib import Path

_SAFE_ID = re.compile(r"[A-Za-z0-9_-]+")


def list_submissions(assignment_id, source):
    """Return every enrolled student with state and attachment_count.

    Reads <source>/<assignment_id>/roster.json and
    submissions/<student_id>/submission.json. Name and email are dropped
    here, so nothing downstream ever sees them.
    """
    root = assignment_dir(assignment_id, source)
    roster = json.loads((root / "roster.json").read_text(encoding="utf-8"))

    records = []
    for student in roster:
        student_id = check_id(student["student_id"])
        folder = root / "submissions" / student_id
        meta = folder / "submission.json"
        if not meta.is_file():
            records.append({"student_id": student_id, "state": "MISSING", "attachment_count": 0})
            continue
        state = json.loads(meta.read_text(encoding="utf-8")).get("state", "TURNED_IN")
        records.append({
            "student_id": student_id,
            "state": state,
            "attachment_count": len(attachments(folder)),
        })
    return sorted(records, key=lambda r: r["student_id"])


def attachments(folder):
    """The files and folders a student attached, in name order."""
    folder = Path(folder) / "attachments"
    if not folder.is_dir():
        return []
    return sorted(folder.iterdir())


def assignment_dir(assignment_id, source):
    return Path(source) / check_id(assignment_id)


def check_id(value):
    """Refuse ids that could point outside their folder."""
    if not isinstance(value, str) or not _SAFE_ID.fullmatch(value):
        raise ValueError(f"unsafe id: {value!r}")
    return value
