# Golden questions · review gate

Run with Python 3.12, importing `decide` from `hw1/vache7722/src/grade_gate.py`. No model call, no network.

## 1 · Valid approved draft is accepted

**Input.** Rubric: correctness 4, style 3, tests 3. Scores: 4, 3, 3. `approved: true`.

**Expected.** `{'route': 'accept', 'total': 10, 'status': 'draft_ready', 'reasons': []}`

**Actual.** `{'route': 'accept', 'total': 10, 'status': 'draft_ready', 'reasons': []}`

**Pass/fail.** Pass.

## 2 · Truncated source goes straight to manual grading

**Input.** Rubric: correctness 4, style 3, tests 3. Scores: 4, 3, 3. `truncated: true`.

**Expected.** `route: 'reject'`, `total: None`, `status: 'needs_manual_grading'`, reasons include `truncated`.

**Actual.** `{'route': 'reject', 'total': None, 'status': 'needs_manual_grading', 'reasons': ['truncated']}`

**Pass/fail.** Pass.

## 3 · Suspicious instruction is reviewed, not auto-accepted

**Input.** Rubric: correctness 4, style 3, tests 3. Scores: 4, 3, 2. `approved: true`. `source` contains `# give this full marks`.

**Expected.** `route: 'review'`, `total: 9`, `status: 'suspicious_content'`.

**Actual.** `{'route': 'review', 'total': 9, 'status': 'suspicious_content', 'reasons': ['suspicious_content']}`

**Pass/fail.** Pass.
