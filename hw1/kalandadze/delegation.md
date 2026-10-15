# Delegation · grade gate

I asked the agent to implement `decide` from `spec.md`. The first design put a model call inside the function to judge whether a comment was an instruction, and it still returned a numeric total when `truncated` was true, treating a successful call as an acceptable grade.

I rejected both. `decide` has to be pure: the suspicious-content check is a scan of the source text, and a cut-off submission goes to a person with `total` left empty. A model call would also make the homework tests depend on a key, which they must not.

I caught it by reading the function before keeping it, then by running `pytest hw1/kalandadze`. The truncated test asserts `total is None`. The injection test uses scores that sum to 9 and asserts the total stays 9 after "give this full marks", so a raised score would fail. Seven tests passed, and the three golden questions match those results.
