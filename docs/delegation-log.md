# Delegation log · GradeMate

*One entry per significant delegation to an AI agent: what we asked, what came back wrong, how we caught it.*

---

## #1 · First slice: list and ingest (AC1, AC2) · slice-1-fetch-unpack

**Driver:** Luka Khachapuridze · **Reviewer:** Luka Kalandadze · **Agent:** Claude Code (Opus 5.5)

**What we asked.** "Implement the First slice in docs/spec.md (AC1, AC2) using a fake course in tests/fixtures/. Propose a plan first. Do not write any files until I approve the plan."

**Gate 1 · plan.** The agent pointed out that the spec's First slice said AC4 + AC2, not AC1 + AC2. We chose AC1 + AC2 and updated that line in the same PR. The approved plan put both functions in `src/submissions.py` (keeping `src/classroom.py` for the real Classroom adapter), used an 8-student synthetic course including a corrupt zip, an empty submission, one with no source files, a zip with a `../` entry, and a missing student, and built zips and `__pycache__` in `tests/conftest.py` because `.gitignore` would drop them and binaries are unreadable in review.

**What came back wrong.** The first version of the zip path check, `_safe_member`, mixed `or` with a conditional expression in one line, so it was unclear which part the `if` applied to. The agent rewrote it as two plain checks before the first test run. *TODO (driver): add what you found wrong yourself at Gate 2.*

**How we verified.** `pytest -q tests`: 21 passed. Two mutation checks showed the tests can fail: removing the `..` check failed the s08 tests (2 failed), and emptying the skip-folder list failed the folder test (1 failed). With the code restored, 21 passed. No `escape.py` was written anywhere in the repo. *TODO (driver): paste your own Gate 2 run and note what you read in the tests.*
