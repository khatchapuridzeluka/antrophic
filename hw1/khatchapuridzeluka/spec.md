# HW1 spec · Approved-grade export

The last step of GradeMate: turn the review table into a CSV the instructor can upload by hand. This covers AC7 and success criterion 4 in `docs/spec.md`. No model call, no network, and nothing is written back to Google Classroom. The only file the function creates is the export itself, plus one log line.

## Input

`export(assignment_id, rubric, rows, out_dir, log_path)` reads:

| Field | Meaning |
|---|---|
| `assignment_id` | Names the file. Letters, digits, `-` and `_` only, so it cannot point outside `out_dir`. |
| `rubric` | List of `{id, max}`. Fixes the score columns and their order. |
| `rows` | One dict per student: `student_id`, `scores` (rubric item id to number), `total`, `approved`. |
| `out_dir` | Folder for exports. The file is `<out_dir>/<assignment_id>.csv`. |
| `log_path` | JSONL file that gets one line per export. |

## Rules

1. **Only approved rows leave.** A row is exported only when `approved` is exactly `true`. `"true"`, `1`, or a missing field is not approval. There is no approve-all.
2. **An approved row still needs a grade.** If `total` is missing or `None` (for example a `needs_manual_grading` draft), or a rubric score is missing, the row is skipped with a reason, not written with blanks.
3. **Fixed columns.** `student_id`, one column per rubric item in rubric order, then `total`. Any other key in a row (a name, an email, feedback) never reaches the file.
4. **No guessing about who is who.** Two rows with the same `student_id` stop the export with an error, and no file is written.
5. **Bad `assignment_id`** (empty, `..`, a slash) stops the export with an error, and no file is written.
6. **One log line** per export: ISO 8601 time in Asia/Tbilisi, `assignment_id`, counts of exported and skipped rows, and the skipped `student_id`s with reasons. No names, no scores.
7. Zero approved rows still writes a header-only CSV, so an empty export is visible rather than missing.

Returned: `{"path", "exported", "skipped"}` where `skipped` is a list of `{student_id, reason}`. Unapproved rows are counted in neither list; they are simply not ready.

## Pass/fail checks

1. 10 approved and 20 unapproved rows: the CSV has exactly 10 data rows (success criterion 4).
2. A row with `approved: "true"` and one with `approved: true` but `total: null`: neither is in the CSV, and the second is reported as skipped with `no_total`.
3. A row that carries `name` and `email`: neither value appears anywhere in the CSV or the log.
