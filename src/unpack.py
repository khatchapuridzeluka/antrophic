import json
import shutil
import zipfile
from pathlib import Path, PurePosixPath

_SOURCE_EXTENSIONS = {".py"}
_SKIP_DIRS = {"__pycache__", "node_modules", ".venv", ".git"}


def ingest(assignment_id, source, work=None):
    """Ingest the assignment into work/<assignment>/<student_id> with only Python source files kept."""
    if not isinstance(assignment_id, str) or not assignment_id.replace("_", "").replace("-", "").isalnum() or assignment_id in {"", ".", ".."}:
        raise ValueError(f"unsafe assignment_id: {assignment_id!r}")

    root = Path(source)
    assignment_root = root / assignment_id
    roster = json.loads((assignment_root / "roster.json").read_text(encoding="utf-8"))

    output_root = Path(work) if work is not None else Path("data") / "work"
    target_dir = output_root / assignment_id
    if target_dir.exists():
        shutil.rmtree(target_dir)

    results = []
    for student in roster:
        student_id = student["student_id"]
        submission_dir = assignment_root / "submissions" / student_id
        dest_dir = target_dir / student_id

        if not submission_dir.exists():
            results.append({"student_id": student_id, "status": "missing", "files": [], "reason": "missing"})
            continue

        attachments_dir = submission_dir / "attachments"
        if not attachments_dir.exists():
            results.append({"student_id": student_id, "status": "unreadable", "files": [], "reason": "empty"})
            continue

        try:
            files = _collect_files(attachments_dir, dest_dir)
        except ValueError as exc:
            if dest_dir.exists():
                shutil.rmtree(dest_dir)
            results.append({"student_id": student_id, "status": "unreadable", "files": [], "reason": str(exc)})
            continue

        if not files:
            if dest_dir.exists():
                shutil.rmtree(dest_dir)
            reason = _reason_for_empty(attachments_dir)
            results.append({"student_id": student_id, "status": "unreadable", "files": [], "reason": reason})
            continue

        results.append({"student_id": student_id, "status": "ok", "files": files})

    return results


def _reason_for_empty(attachments_dir):
    if not any(attachments_dir.iterdir()):
        return "empty"
    for path in attachments_dir.rglob("*"):
        if path.is_file() and path.suffix.lower() == ".py":
            return "no_source_files"
        if path.suffix.lower() in {".md", ".png", ".jpg", ".jpeg"}:
            pass
    return "no_source_files"


def _collect_files(attachments_dir, dest_dir):
    entries = sorted(p for p in attachments_dir.iterdir())
    if not entries:
        return []

    if len(entries) == 1 and entries[0].is_file() and entries[0].suffix.lower() == ".zip":
        return _extract_zip(entries[0], dest_dir)

    if len(entries) == 1 and entries[0].is_file() and entries[0].suffix.lower() == ".py":
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest_file = dest_dir / entries[0].name
        shutil.copy2(entries[0], dest_file)
        return [entries[0].name]

    source_files = _iter_source_files(attachments_dir)
    if not source_files:
        return []

    dest_dir.mkdir(parents=True, exist_ok=True)
    for source_file in source_files:
        rel = source_file.relative_to(attachments_dir)
        target = dest_dir / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_file, target)

    relative_paths = [p.relative_to(dest_dir).as_posix() for p in dest_dir.rglob("*") if p.is_file()]
    return sorted(relative_paths)


def _iter_source_files(root):
    files = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in _SKIP_DIRS for part in path.parts):
            continue
        if path.suffix.lower() in _SOURCE_EXTENSIONS:
            files.append(path)
    return sorted(files)


def _extract_zip(zip_path, dest_dir):
    try:
        with zipfile.ZipFile(zip_path, "r") as zf:
            members = zf.infolist()
            extracted = []
            for info in members:
                name = info.filename.replace("\\", "/")
                pure = PurePosixPath(name)
                if pure.is_absolute() or ".." in pure.parts:
                    raise ValueError("unsafe_archive")
                if info.is_dir():
                    continue
                suffix = PurePosixPath(name).suffix.lower()
                if suffix != ".py":
                    continue
                target = dest_dir / pure
                target.parent.mkdir(parents=True, exist_ok=True)
                with zf.open(info, "r") as src, target.open("wb") as dst:
                    shutil.copyfileobj(src, dst)
                extracted.append(target.relative_to(dest_dir).as_posix())
            if not extracted:
                return []
            return sorted(extracted)
    except zipfile.BadZipFile:
        raise ValueError("corrupt_archive")
