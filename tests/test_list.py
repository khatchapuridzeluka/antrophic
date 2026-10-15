import json

import pytest

from conftest import ROSTER_SECRETS
from src.fetch import list_submissions


def test_every_enrolled_student_is_listed_in_order(course):
    records = list_submissions("a01", course)

    assert [r["student_id"] for r in records] == [f"s0{n}" for n in range(1, 9)]


def test_student_without_a_submission_is_missing(course):
    records = {r["student_id"]: r for r in list_submissions("a01", course)}

    assert records["s07"] == {"student_id": "s07", "state": "MISSING", "attachment_count": 0}


def test_state_and_attachment_count_come_from_the_drop(course):
    records = {r["student_id"]: r for r in list_submissions("a01", course)}

    assert records["s03"]["state"] == "LATE"
    assert records["s03"]["attachment_count"] == 1
    assert records["s01"]["state"] == "TURNED_IN"
    assert records["s01"]["attachment_count"] == 1
    assert records["s05"]["attachment_count"] == 0
    assert records["s06"]["attachment_count"] == 2


def test_name_and_email_never_leave_the_list(course):
    records = list_submissions("a01", course)

    assert all(set(r) == {"student_id", "state", "attachment_count"} for r in records)
    dumped = json.dumps(records)
    for secret in ROSTER_SECRETS:
        assert secret not in dumped


@pytest.mark.parametrize("bad_id", ["", "..", "../a01", "a01/x"])
def test_unsafe_assignment_id_is_refused(course, bad_id):
    with pytest.raises(ValueError, match="unsafe"):
        list_submissions(bad_id, course)
