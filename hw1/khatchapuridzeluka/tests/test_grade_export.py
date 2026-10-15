import csv
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from grade_export import export

RUBRIC = [
    {"id": "correctness", "max": 4},
    {"id": "style", "max": 3},
    {"id": "tests", "max": 3},
]


def _row(student_id, approved=True, **overrides):
    row = {
        "student_id": student_id,
        "scores": {"correctness": 4, "style": 3, "tests": 2},
        "total": 9,
        "approved": approved,
    }
    row.update(overrides)
    return row


def _run(tmp_path, rows, assignment_id="hw1"):
    out_dir = tmp_path / "exports"
    log_path = tmp_path / "logs" / "exports.jsonl"
    result = export(assignment_id, RUBRIC, rows, out_dir, log_path)
    return result, out_dir, log_path


def _csv_rows(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.reader(f))


def test_ten_approved_and_twenty_unapproved_export_exactly_ten(tmp_path):
    rows = [_row(f"s{n:02d}", approved=n <= 10) for n in range(1, 31)]

    result, out_dir, _ = _run(tmp_path, rows)

    lines = _csv_rows(out_dir / "hw1.csv")
    assert lines[0] == ["student_id", "correctness", "style", "tests", "total"]
    assert [line[0] for line in lines[1:]] == [f"s{n:02d}" for n in range(1, 11)]
    assert result["exported"] == 10
    assert result["skipped"] == []


def test_truthy_but_not_true_is_not_approval(tmp_path):
    rows = [_row("s01", approved="true"), _row("s02", approved=1), _row("s03", approved=None)]

    result, out_dir, _ = _run(tmp_path, rows)

    assert _csv_rows(out_dir / "hw1.csv") == [["student_id", "correctness", "style", "tests", "total"]]
    assert result["exported"] == 0


def test_approved_row_without_a_total_is_skipped_with_a_reason(tmp_path):
    rows = [_row("s01"), _row("s02", total=None), _row("s03", scores={"correctness": 4, "style": 3})]

    result, out_dir, _ = _run(tmp_path, rows)

    assert [line[0] for line in _csv_rows(out_dir / "hw1.csv")[1:]] == ["s01"]
    assert result["skipped"] == [
        {"student_id": "s02", "reason": "no_total"},
        {"student_id": "s03", "reason": "missing:tests"},
    ]


def test_name_and_email_never_reach_the_csv_or_the_log(tmp_path):
    rows = [_row("s01", name="Nino Beridze", email="nino@example.com", feedback="good")]

    _, out_dir, log_path = _run(tmp_path, rows)

    written = (out_dir / "hw1.csv").read_text(encoding="utf-8") + log_path.read_text(encoding="utf-8")
    assert "Nino" not in written
    assert "nino@example.com" not in written
    assert "good" not in written


def test_duplicate_student_id_stops_the_export_before_writing(tmp_path):
    rows = [_row("s01"), _row("s01", total=7)]

    with pytest.raises(ValueError, match="duplicate"):
        _run(tmp_path, rows)

    assert not (tmp_path / "exports").exists()


@pytest.mark.parametrize("bad_id", ["", "..", "../hw1", "hw1/x", "hw 1"])
def test_unsafe_assignment_id_stops_the_export_before_writing(tmp_path, bad_id):
    with pytest.raises(ValueError, match="unsafe"):
        _run(tmp_path, [_row("s01")], assignment_id=bad_id)

    assert not (tmp_path / "exports").exists()


def test_export_writes_one_log_line_in_tbilisi_time(tmp_path):
    rows = [_row("s01"), _row("s02", total=None), _row("s03", approved=False)]

    _, _, log_path = _run(tmp_path, rows)

    lines = log_path.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 1
    entry = json.loads(lines[0])
    assert entry["time"].endswith("+04:00")
    assert entry["assignment_id"] == "hw1"
    assert entry["exported"] == 1
    assert entry["skipped"] == [{"student_id": "s02", "reason": "no_total"}]


def test_export_does_not_touch_the_source_drop(tmp_path):
    drop = tmp_path / "drop"
    drop.mkdir()
    (drop / "s01.py").write_text("print('hi')\n", encoding="utf-8")
    before = {p.name: p.read_bytes() for p in drop.iterdir()}

    _run(tmp_path, [_row("s01")])

    assert {p.name: p.read_bytes() for p in drop.iterdir()} == before
