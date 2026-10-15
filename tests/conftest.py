import shutil
import sys
import zipfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

FIXTURE_COURSE = Path(__file__).parent / "fixtures" / "course"

# Fake fixture students whose names and emails must never leave list_submissions.
ROSTER_SECRETS = ["Test Student", "@example.test"]


@pytest.fixture
def course(tmp_path):
    """A copy of the synthetic course, with the files git cannot hold added.

    Zips, __pycache__ and binary-looking files are built here so the committed
    fixture stays plain text and readable in review.
    """
    source = tmp_path / "course"
    shutil.copytree(FIXTURE_COURSE, source)
    subs = source / "hw1" / "submissions"

    project = subs / "s02" / "attachments" / "project"
    (project / "__pycache__").mkdir()
    (project / "__pycache__" / "utils.cpython-311.pyc").write_bytes(b"\x00compiled")
    (project / "node_modules" / "left-pad").mkdir(parents=True)
    (project / "node_modules" / "left-pad" / "index.py").write_text("x = 1\n")
    (project / "diagram.png").write_bytes(b"\x89PNG fake")

    (subs / "s03" / "attachments").mkdir()
    with zipfile.ZipFile(subs / "s03" / "attachments" / "hw.zip", "w") as zf:
        zf.writestr("pkg/a.py", "def a():\n    return 1\n")
        zf.writestr("pkg/notes.txt", "not source\n")

    (subs / "s06" / "attachments" / "screenshot.png").write_bytes(b"\x89PNG fake")

    (subs / "s08" / "attachments").mkdir()
    with zipfile.ZipFile(subs / "s08" / "attachments" / "evil.zip", "w") as zf:
        zf.writestr("ok.py", "print('fine')\n")
        zf.writestr("../escape.py", "print('escaped')\n")

    return source
