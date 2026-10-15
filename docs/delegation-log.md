# Delegation log · GradeMate

*One entry per significant delegation to an AI agent: what we asked, what came back wrong, how we caught it.*

---

## #1 · First slice: list and ingest (AC1, AC2) · slice-1-fetch-unpack

**Driver:** Luka Khachapuridze · **Reviewer:** Luka Kalandadze · **Agent:** Claude Code (Opus 5.5)

**What we asked.** "Implement the First slice in docs/spec.md (AC1, AC2) using a fake course in tests/fixtures/. Propose a plan first. Do not write any files until I approve the plan."

**Gate 1 · plan.** The agent pointed out that the spec's First slice said AC4 + AC2, not AC1 + AC2. We chose AC1 + AC2 and updated that line in the same PR. The approved plan used an 8-student synthetic course including a corrupt zip, an empty submission, one with no source files, a zip with a `../` entry, and a missing student.

**What came back wrong.**
- The first zip path check, `_safe_member`, mixed `or` with a conditional expression in one line, so it was unclear which part the `if` applied to. The agent rewrote it as two plain checks before the first test run.
- Gate 2 review found more:
  - The zips existed only inside `tests/conftest.py`, so the committed course and the tests disagreed. In a demo, s03 (`LATE`, 0 attachments) came out `empty` and s08 came out `empty`, while the tests said `ok` and `unsafe_archive`.
  - The issue asked for `src/fetch.py` and `src/unpack.py`, but the agent created a single `src/submissions.py`.
  - The `.py`-only rule was new and written down nowhere.
  - The agent's own explanation linked the slice to the HW1 folders, which team code must not do.
- Fixes:
  - The zips, `node_modules/` and image files are now committed, and `tests/fixtures/course/README.md` lists every case.
  - The code is split into `fetch.py` and `unpack.py`.
  - Decision 0003, spec AC2 and `AGENTS.md` now state the `.py`-only rule.
  - `AGENTS.md` forbids imports from `hw1/` and `hw2/`.
  - The fake assignment is renamed `a01`.
- One review point was not a code bug: the demo wrote to a temporary folder passed in by hand, while the default really is `data/work/`. A test now pins that default.

**How we verified.**
- `pytest -q tests`: 22 passed.
- Three mutation checks showed the tests can fail:
  - Removing the `..` check failed 2 s08 tests.
  - Emptying the skip-folder list failed the folder test.
  - Changing the default to `work` failed the new default-folder test.
- With the code restored, all 22 passed.
- A demo `ingest` on the committed course gives the same 8 results as the tests, and no `escape.py` was written anywhere.
- *TODO (driver): paste your own Gate 2 run.*
