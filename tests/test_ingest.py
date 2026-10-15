from pathlib import Path

import pytest

from src.unpack import ingest


def _files(folder):
    return sorted(p.relative_to(folder).as_posix() for p in Path(folder).rglob("*") if p.is_file())


@pytest.fixture
def run(course, tmp_path):
    work = tmp_path / "work"
    results = {r["student_id"]: r for r in ingest("a01", course, work)}
    return results, work / "a01"


def test_run_finishes_with_one_result_per_student(run):
    results, _ = run

    assert sorted(results) == [f"s0{n}" for n in range(1, 9)]


def test_single_file_is_ingested(run):
    results, work = run

    assert results["s01"]["status"] == "ok"
    assert _files(work / "s01") == ["solution.py"]


def test_folder_keeps_only_source_files(run):
    results, work = run

    assert results["s02"]["status"] == "ok"
    assert _files(work / "s02") == ["project/main.py", "project/utils.py"]
    assert results["s02"]["files"] == ["project/main.py", "project/utils.py"]


def test_zip_is_unpacked_to_source_files(run):
    results, work = run

    assert results["s03"]["status"] == "ok"
    assert _files(work / "s03") == ["pkg/a.py"]


@pytest.mark.parametrize(
    "student_id, reason",
    [
        ("s04", "corrupt_archive"),
        ("s05", "empty"),
        ("s06", "no_source_files"),
        ("s08", "unsafe_archive"),
    ],
)
def test_bad_submission_is_unreadable_and_leaves_no_files(run, student_id, reason):
    results, work = run

    assert results[student_id]["status"] == "unreadable"
    assert results[student_id]["reason"] == reason
    assert results[student_id]["files"] == []
    assert not (work / student_id).exists()


def test_missing_student_is_not_unreadable(run):
    results, work = run

    assert results["s07"]["status"] == "missing"
    assert not (work / "s07").exists()


def test_zip_slip_writes_nothing_outside_the_work_folder(run, tmp_path):
    escaped = [p for p in tmp_path.rglob("escape.py")]

    assert escaped == []


def test_default_output_is_data_work(course, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    ingest("a01", course)

    assert _files(tmp_path / "data" / "work" / "a01" / "s01") == ["solution.py"]


def test_rerun_gives_the_same_files(course, tmp_path):
    work = tmp_path / "work"
    ingest("a01", course, work)
    (work / "a01" / "s01" / "stale.py").write_text("old\n")

    ingest("a01", course, work)

    assert _files(work / "a01" / "s01") == ["solution.py"]


def test_ingest_does_not_change_the_source_drop(course, tmp_path):
    before = {p: p.read_bytes() for p in course.rglob("*") if p.is_file()}

    ingest("a01", course, tmp_path / "work")

    assert {p: p.read_bytes() for p in course.rglob("*") if p.is_file()} == before
