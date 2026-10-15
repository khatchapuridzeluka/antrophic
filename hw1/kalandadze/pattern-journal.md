# Pattern Journal · Luka Kalandadze

*One entry per teaching week, 2 to 3 sentences. Graded inside HW1 (W1-4), HW2 (W5-7), and the Repository Review (W10-14). Honest beats polished.*

Format per entry:
**W# · [Pattern name]** · Where I applied it · What I delegated to AI · How I verified it

---

**W1 · Context as Budget** · Applied in GradeMate's context list: the model sees the brief, the rubric, source capped at about 6,000 tokens, and a student id. Names, emails, binaries, `node_modules`, and `.venv` stay out. I delegated a first draft of that list; it wanted the whole submission archive and the classroom record in the prompt. We rejected both, because the grade does not need them and a name in the prompt is a privacy leak. Verified by checking every acceptance criterion against the list: nothing the model must do depends on a field we cut. Next time I would count tokens on one fixture file before writing 7,000 into the napkin math.

**W2 · Spec Before Code** ·I applied it in `docs/spec.md`, where I delegated listing the three biggest ambiguities and rewriting GradeMate's success criteria so each one is measurable. I rejected the proposal to replace the 15-minute live-run bound with a p95 latency check in CI, because those tests must not call the model and would not measure a 30-submission run. I kept the wall-clock record in `evals/results/` and checked that each of the four criteria names an input, a threshold, and where the number is read.

**W3 · Uncertainty-Aware UX** · Applied in the grade draft, not in a confidence number the model gives itself. A truncated submission or a grade JSON that fails `schemas/grade.json` is `needs_manual_grading`, and the total is left empty instead of prefilled. I delegated the policy wording; the draft treated a successful model call as an acceptable grade. That fails the lab: empty or cut-off input goes to a person, and `decide()` must be a pure function with no model call inside. Verified by reading AC4 and checking the row a human sees is blank on those cases. Next time I would write the four routes (accept, confirm, review, reject) in `docs/confidence-policy.md` before asking an agent to implement `decide()`.

**W4 · Grounded Generation** · Applied by making the rubric the source the feedback has to cite: every feedback point names a rubric item id, test results are context rather than the score, and a claim the code does not support is a failed check. I delegated a first pass at the criteria; it would have graded from the test count alone, which is arithmetic and needs no model. Verified by adding AC5 (tests all pass, a named rubric item still loses points) and by keeping the refusal in the spec: a bad or missing citation does not ship as a warning. The five-question golden set is not run yet. Next time I would write `evals/golden.yaml` (two factual, one that needs the brief and the rubric, one edge case, one refusal) before the retrieval code, so a failing question gets fixed instead of deleted.
