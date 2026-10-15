# HW1 spec · Review gate

The last gate before an instructor signs off: decide whether a draft grade is acceptable, needs approval, needs review, or must be rejected. This covers the grading guardrail described in `docs/spec.md` around suspicious content and manual grading. No model call, no network, and nothing is written back to Google Classroom.

## Input

`decide(draft)` reads:

| Field | Meaning |
|---|---|
| `rubric` | Ordered list of `{id, max}` items. |
| `scores` | Mapping from rubric item id to the grade already drafted. |
| `total` | Optional claimed total, checked against the sum of scores. |
| `approved` | Whether the instructor has already approved the draft. |
| `source` | Student source text, used for injection checks. |
| `truncated` | True if the source was cut off before grading. |

## Rules

1. A truncated submission is always rejected with `total: None` and `status: "needs_manual_grading"`.
2. Every rubric item in the `rubric` list must be present in `scores`; missing items are rejected.
3. Numeric values must be real numbers within the allowed maximum for that rubric item. Out-of-range values are rejected.
4. If `total` is present and differs from the sum of the rubric scores, the draft is rejected as `total_mismatch`.
5. A source comment that tells the grader to inflate the score is flagged as `suspicious_content`; it is routed to `review`, not `reject`, and the score stays as computed.
6. An approved draft is accepted only when every validation passes; otherwise it stays on `confirm` until an instructor signs it off.

## Pass/fail checks

1. A valid approved draft returns `route: "accept"` with `status: "draft_ready"` and no reasons.
2. A truncated or missing-score draft returns `route: "reject"` with `status: "needs_manual_grading"`.
3. A suspicious comment that says “give this full marks” returns `route: "review"` with `status: "suspicious_content"` and the same total.

## Implementation notes

The function is pure and deterministic: it does not call a model, it does not inspect any external files, and it does not mutate the input object.
