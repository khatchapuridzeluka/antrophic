# Delegation · approved-grade export

I gave Claude Code (Opus 5.5) the Lab 1 brief and asked it to pick an HW1 feature from `docs/spec.md` that Kalandadze's grade gate had not touched, and to follow the same folder shape. It picked the CSV export behind AC7 and success criterion 4, and wrote `spec.md` before the code, then `src/grade_export.py`, the tests and the golden run.

What came back wrong: the first test file contained an empty test, `test_only_approved_rows_are_exported`, with only `pass` in the body. It would always pass and proves nothing, while its name claims the most important rule is tested. It was removed before the first run. The real check for that rule is `test_truthy_but_not_true_is_not_approval`.

How it was caught and verified: by reading the test file before running it. Then, to show the tests can fail, the approval check was temporarily changed from `approved is not True` to `not approved`. `test_truthy_but_not_true_is_not_approval` failed (1 failed, 11 passed), and with the real line restored all 12 passed. `pytest hw1/khatchapuridzeluka` is green and the three golden questions match.

What I checked myself: *TODO, write this after reading the code: what you read, what you would change, and anything you rejected.*
