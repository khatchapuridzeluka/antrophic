import json
import re
from pathlib import Path

_SAFE_ASSIGNMENT = re.compile(r"^[A-Za-z0-9_-]+$")


def list_submissions(assignment_id, source):
    """Return roster rows for an assignment, exposing only student_id/state/attachment_count."""
    if not isinstance(assignment_id, str) or not _SAFE_ASSIGNMENT.fullmatch(assignment_id):
        raise ValueError(f"unsafe assignment_id: {assignment_id!r}")

    root = Path(source)
    roster_path = root / assignment_id / "roster.json"
    submissions_dir = root / assignment_id / "submissions"

    roster = json.loads(roster_path.read_text(encoding="utf-8"))
    records = []

    for student in roster:
        student_id = student["student_id"]
        submission_dir = submissions_dir / student_id
        if not submission_dir.exists():
            records.append({"student_id": student_id, "state": "MISSING", "attachment_count": 0})
            continue

        submission_json = submission_dir / "submission.json"
        state = "MISSING"
        if submission_json.exists():
            with submission_json.open("r", encoding="utf-8") as fh:
                payload = json.load(fh)
            state = payload.get("state", "MISSING")

        attachments_dir = submission_dir / "attachments"
        attachment_count = 0
        if attachments_dir.exists():
            attachment_count = sum(1 for p in attachments_dir.rglob("*") if p.is_file())

        records.append({
            "student_id": student_id,
            "state": state,
            "attachment_count": attachment_count,
        })

    return records
