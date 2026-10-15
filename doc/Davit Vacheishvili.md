# Davit Vacheishvili

## Pattern Journal

Weeks 1–4

One entry per week, 2 to 3 sentences: pattern · where I applied it · what I delegated to AI · how I verified it.

### Week 1 · Context as Budget
Applied while scoping the grading problem in the team spec: the model sees only the assignment brief, rubric, test results, and a capped slice of source files, identified by student ID only. I delegated the first draft of the context list and the napkin-math estimate to Claude, then verified each item by checking it was required by at least one acceptance criterion.

### Week 2 · Spec Before Code
The team wrote the repo rules and product spec before implementation so the backlog stayed testable. I delegated the draft spec and AGENTS setup to the agent and then reviewed the details against the course rules to make sure each criterion could be checked by a script.

### Week 3 · Uncertainty-Aware UX
The grade gate is the example of “not sure” behavior: the app does not guess when a draft looks suspicious or incomplete. I delegated the decision logic and the unit tests to the agent and verified each branch by reading the logic and checking the route outputs.

### Week 4 · Grounded Generation
Grounded evaluation means the score must match the rubric and the evidence, not a model's intuition. I delegated the rule draft and golden checks to the agent and verified the pass/fail results by reading the code paths and checking the expected review and reject behavior.
