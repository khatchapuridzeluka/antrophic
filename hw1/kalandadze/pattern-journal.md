# Pattern Journal · Luka Kalandadze

*One entry per teaching week, 2 to 3 sentences. Graded inside HW1 (W1-4), HW2 (W5-7), and the Repository Review (W10-14). Honest beats polished.*

Format per entry:
**W# · [Pattern name]** · Where I applied it · What I delegated to AI · How I verified it

---

**W1 · Context as Budget** ·

**W2 · Spec Before Code** · I applied it in `docs/spec.md`, where I delegated listing the three biggest ambiguities and rewriting GradeMate's success criteria so each one is measurable. I rejected the proposal to replace the 15-minute live-run bound with a p95 latency check in CI, because those tests must not call the model and would not measure a 30-submission run. I kept the wall-clock record in `evals/results/` and checked that each of the four criteria names an input, a threshold, and where the number is read.

**W3 · Uncertainty-Aware UX** ·

**W4 · Grounded Generation** ·
