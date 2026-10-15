# Pattern Journal · Davit Vacheishvili

*One entry per week, 2 to 3 sentences: pattern · where I applied it · what I delegated to AI · how I verified it.*

## Week 1 · Context as Budget
Applied while scoping the grading problem in `docs/spec.md`: the model sees only the assignment brief, rubric, test results and source files, all identified by a synthetic `student_id` so names and emails never reach prompts. I delegated the draft version of the context list and the napkin-math estimate to Claude, then verified each item by checking that it was needed by one acceptance criterion or a concrete risk. The result is a tighter prompt budget that keeps the AI focused on grading and not on student identity.

## Week 2 · Spec Before Code
Our team wrote the repo rules and the product spec before writing the first implementation, which kept the backlog checkable and testable. I delegated the spec draft, the repo structure, and the first version of `AGENTS.md`, then verified that each acceptance criterion could be decided by a script instead of a subjective reading. This is what made the later grade-gate work easier to implement and review.

## Week 3 · Uncertainty-Aware UX
The grade-gate feature is the place where the app says “not sure” instead of guessing: a suspicious or invalid draft is routed to review, rejected, or held for manual grading. I delegated the first pass of the decision logic and the test set to Claude, then checked every branch in the code by reading the logic and verifying each route with a targeted test. The low-confidence path is intentional and explicit, which is safer than silently inflating a score.

## Week 4 · Grounded Generation
This week I applied the same discipline to the grading decision itself: the result must be grounded in the rubric and the source, and any instruction to “give full marks” is flagged instead of accepted. I delegated the first cut of the rule set and the golden checks to Claude, then verified the route logic with direct assertions on the function output. The model is not allowed to rewrite the score without evidence, and that is exactly what the gate protects.
