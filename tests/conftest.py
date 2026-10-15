import shutil
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

FIXTURE_COURSE = Path(__file__).parent / "fixtures" / "course"

# Fake fixture students whose names and emails must never leave list_submissions.
ROSTER_SECRETS = ["Test Student", "@example.test"]


@pytest.fixture
def course(tmp_path):
    """A copy of the committed fake course (tests/fixtures/course/README.md).

    Tests work on the copy so they can prove the source drop is never changed.
    """
    source = tmp_path / "course"
    shutil.copytree(FIXTURE_COURSE, source)
    return source
