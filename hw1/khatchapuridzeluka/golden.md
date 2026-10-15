# Golden questions · approved-grade export

Run with Python 3.12, importing `export` from `hw1/khatchapuridzeluka/src/grade_export.py` and writing to a temporary folder. No model and no network. Actual values below are from that run.

Rubric for every question: correctness max 4, style max 3, tests max 3. Unless a question says otherwise, each row has scores 4, 3, 2 and total 9.

## 1 · Only approved rows leave

**Input.** 30 rows, `s01` to `s30`. `s01` to `s10` have `approved` true, `s11` to `s30` have `approved` false. Assignment `q1`.

**Expected.** The CSV has exactly 10 data rows. `exported` 10, nothing skipped.

**Actual.** `{'exported': 10, 'skipped': [], 'data_rows': 10}`

**Pass/fail.** Pass.

## 2 · Almost-approved is not approved

**Input.** `s01` has `approved` set to the string `"true"`. `s02` has `approved` true but `total` null, as a `needs_manual_grading` draft would. Assignment `q2`.

**Expected.** Header-only CSV. `exported` 0. `s01` is not mentioned (it is not approved), `s02` is skipped with `no_total`.

**Actual.** `{'exported': 0, 'skipped': [{'student_id': 's02', 'reason': 'no_total'}]}`, CSV `'student_id,correctness,style,tests,total\n'`

**Pass/fail.** Pass.

## 3 · A name never reaches the file

**Input.** One approved row `s01` that also carries `name` "Nino Beridze" and `email` "nino@example.com" (synthetic). Assignment `q3`.

**Expected.** CSV is `student_id,correctness,style,tests,total` then `s01,4,3,2,9`. Neither the name nor the email appears in the CSV or the log.

**Actual.** `'student_id,correctness,style,tests,total\ns01,4,3,2,9\n'`, `{'name_found': False, 'email_found': False}`

**Pass/fail.** Pass.
