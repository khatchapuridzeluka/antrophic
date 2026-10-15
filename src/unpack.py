"""Unpack submissions into source folders (AC2).

Student files are treated as data: they are copied, never imported or run.
Only .py files are kept (docs/decisions/0003).
"""

import shutil
import zipfile
from pathlib import Path, PurePosixPath

from src.fetch import assignment_dir, attachments, list_submissions

SOURCE_SUFFIXES = {".py"}
SKIP_DIRS = {"__pycache__", "node_modules", ".venv", "venv", ".git"}
MAX_ZIP_ENTRIES = 200
MAX_ZIP_BYTES = 5 * 1024 * 1024


class Unreadable(Exception):
    """A submission that cannot be turned into source files."""


def ingest(assignment_id, source, work_root="data/work"):
    """Copy each submission's source files to <work_root>/<assignment>/<student_id>/.

    Returns one result per enrolled student. A bad submission is marked
    unreadable and the run continues.
    """
    root = assignment_dir(assignment_id, source)
    results = []
    for record in list_submissions(assignment_id, source):
        student_id = record["student_id"]
        if record["state"] == "MISSING":
            results.append(_result(student_id, "missing", "missing"))
            continue

        target = Path(work_root) / assignment_id / student_id
        if target.exists():
            shutil.rmtree(target)
        target.mkdir(parents=True)
        try:
            files = _ingest_one(attachments(root / "submissions" / student_id), target)
        except Unreadable as exc:
            shutil.rmtree(target, ignore_errors=True)
            results.append(_result(student_id, "unreadable", str(exc)))
        except Exception:
            shutil.rmtree(target, ignore_errors=True)
            results.append(_result(student_id, "unreadable", "error"))
        else:
            results.append(_result(student_id, "ok", None, files))
    return results


def _ingest_one(items, target):
    if not items:
        raise Unreadable("empty")

    for attachment in items:
        if attachment.is_dir():
            _copy_tree(attachment, target / attachment.name)
        elif attachment.suffix.lower() == ".zip":
            _extract_zip(attachment, target)
        elif attachment.suffix.lower() in SOURCE_SUFFIXES:
            shutil.copyfile(attachment, target / attachment.name)

    files = sorted(p.relative_to(target).as_posix() for p in target.rglob("*") if p.is_file())
    if not files:
        raise Unreadable("no_source_files")
    return files


def _copy_tree(src_dir, dest_dir):
    for path in src_dir.rglob("*"):
        rel = path.relative_to(src_dir)
        if any(part in SKIP_DIRS for part in rel.parts):
            continue
        if path.is_file() and not path.is_symlink() and path.suffix.lower() in SOURCE_SUFFIXES:
            out = dest_dir / rel
            out.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(path, out)


def _extract_zip(archive, target):
    try:
        with zipfile.ZipFile(archive) as zf:
            entries = zf.infolist()
            if len(entries) > MAX_ZIP_ENTRIES or sum(e.file_size for e in entries) > MAX_ZIP_BYTES:
                raise Unreadable("too_large")
            for entry in entries:
                if not _safe_member(entry.filename):
                    raise Unreadable("unsafe_archive")
            for entry in entries:
                rel = PurePosixPath(entry.filename)
                if entry.is_dir() or any(part in SKIP_DIRS for part in rel.parts):
                    continue
                if rel.suffix.lower() not in SOURCE_SUFFIXES:
                    continue
                out = target / Path(*rel.parts)
                out.parent.mkdir(parents=True, exist_ok=True)
                out.write_bytes(zf.read(entry))
    except zipfile.BadZipFile:
        raise Unreadable("corrupt_archive")


def _safe_member(name):
    path = PurePosixPath(name.replace("\\", "/"))
    if path.is_absolute() or ".." in path.parts:
        return False
    # A drive letter such as "C:" would escape the target on Windows.
    return not (path.parts and ":" in path.parts[0])


def _result(student_id, status, reason, files=None):
    return {"student_id": student_id, "status": status, "reason": reason, "files": files or []}
