# Pattern Journal · luka khachapuridze

*One entry per week, 2 to 3 sentences: pattern · where I applied it · what I delegated to AI · how I verified it.*

## Week 1 · Context as Budget
Applied in the context list of our team spec (`docs/spec.md`): the grading model sees only the assignment brief, the rubric, the test results and the student's source files capped at about 6,000 tokens, identified by student ID only, never name or email. I delegated the first draft of the context list and the napkin math (about $2.60/month for 240 submissions) to Claude. I checked that every item in the list is needed by at least one acceptance criterion, and noted that the prices in the napkin math are placeholders until we pick a model and measure real usage in `logs/usage.jsonl`.

## Week 2 · Spec Before Code
Our team wrote `docs/spec.md` and `AGENTS.md` before any code existed, starting from Vache's real problem of grading Google Classroom zips by hand. I delegated the spec draft, `AGENTS.md`, the team contract and the repo setup files to Claude, and did not accept them blindly: I asked what each file is for and questioned whether `pytest.ini` was needed at all, since CI already runs `pytest -q tests`. Verified by checking each acceptance criterion could be decided by a script, and as a result we changed the test command in `AGENTS.md` to `pytest -q tests` so the agent, CI and a plain local run all test the same folder.

## Week 3 · Uncertainty-Aware UX
*To write after the Lab 3 feature.* (Where the app says "not sure" instead of guessing, what I delegated, and how I tested the low-confidence path.)

## Week 4 · Grounded Generation
*To write after Lab 4 or my HW1 feature.* (Where answers come from our own documents with citations, what I delegated, and how a golden question verified it.)