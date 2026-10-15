# Delegation · review gate

I delegated the first draft of the grade-gate logic to Claude and asked it to stay inside the HW1 constraints: pure Python, no model call, no network, no write-back. The first pass was broad and included a few unnecessary checks, but the central pattern was correct: validate the rubric, identify the suspicious prompt injection, and route the result to a human review path.

What came back wrong: the draft included a rule that treated any `approved` field as truthy, which would accept strings like `"true"` and silently bypass the approval gate. I caught that by reading the code before running it and by checking the acceptance criteria for the exact rules around `approved` and manual grading.

How I verified it: I ran the local tests and then changed the `approved` logic in one temporary branch to confirm the failing assertion. The tests caught the issue immediately, and after restoring the correct logic the full file passed. I also checked the suspicious-content route stays at the same total instead of raising the grade.
