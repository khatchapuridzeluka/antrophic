"""Export approved grades to CSV. No model call, no network, no write-back."""

import csv
import json
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path

# Georgia has no daylight saving time, so Asia/Tbilisi is a fixed UTC+4.
TBILISI = timezone(timedelta(hours=4), "Asia/Tbilisi")

_SAFE_ID = re.compile(r"[A-Za-z0-9_-]+")


def export(assignment_id, rubric, rows, out_dir, log_path):
    """Write <out_dir>/<assignment_id>.csv with approved rows only.

    Only student_id, the rubric scores and total are written. Duplicate
    student ids or an unsafe assignment id raise ValueError before any file
    is touched.
    """
    if not isinstance(assignment_id, str) or not _SAFE_ID.fullmatch(assignment_id):
        raise ValueError(f"unsafe assignment_id: {assignment_id!r}")

    item_ids = [item["id"] for item in rubric]
    ids = [row.get("student_id") for row in rows]
    duplicates = sorted({sid for sid in ids if ids.count(sid) > 1}, key=str)
    if duplicates:
        raise ValueError(f"duplicate student_id: {duplicates}")

    exported, skipped = [], []
    for row in rows:
        if row.get("approved") is not True:
            continue
        reason = _not_exportable(row, item_ids)
        if reason:
            skipped.append({"student_id": row.get("student_id"), "reason": reason})
            continue
        exported.append(row)

    path = Path(out_dir) / f"{assignment_id}.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["student_id", *item_ids, "total"])
        for row in exported:
            scores = row["scores"]
            writer.writerow([row["student_id"], *(scores[i] for i in item_ids), row["total"]])

    _log(log_path, assignment_id, len(exported), skipped)
    return {"path": str(path), "exported": len(exported), "skipped": skipped}


def _not_exportable(row, item_ids):
    if not row.get("student_id"):
        return "no_student_id"
    if row.get("total") is None:
        return "no_total"
    scores = row.get("scores") or {}
    for item_id in item_ids:
        if item_id not in scores:
            return f"missing:{item_id}"
    return None


def _log(log_path, assignment_id, exported, skipped):
    entry = {
        "time": datetime.now(TBILISI).isoformat(timespec="seconds"),
        "event": "export",
        "assignment_id": assignment_id,
        "exported": exported,
        "skipped": skipped,
    }
    log_path = Path(log_path)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")
