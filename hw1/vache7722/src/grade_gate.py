"""Pure grade gate. No model call and no network."""

_GRADER_INSTRUCTIONS = (
    "give this full marks",
    "give me full marks",
    "ignore previous",
    "ignore the rubric",
    "you are the grader",
    "award full marks",
)


def decide(draft):
    """Route one draft to accept, confirm, review, or reject.

    A rejected draft always has total None. A suspicious comment does not
    raise the score.
    """
    total, problems = _problems(draft)
    if problems:
        return {
            "route": "reject",
            "total": None,
            "status": "needs_manual_grading",
            "reasons": problems,
        }

    if _suspicious(draft.get("source") or ""):
        return {
            "route": "review",
            "total": total,
            "status": "suspicious_content",
            "reasons": ["suspicious_content"],
        }

    if draft.get("approved"):
        return {
            "route": "accept",
            "total": total,
            "status": "draft_ready",
            "reasons": [],
        }

    return {
        "route": "confirm",
        "total": total,
        "status": "draft_ready",
        "reasons": ["not_approved"],
    }


def _problems(draft):
    if draft.get("truncated"):
        return None, ["truncated"]

    rubric = draft.get("rubric") or []
    if not rubric:
        return None, ["empty_rubric"]

    scores = draft.get("scores") or {}
    problems = []
    total = 0
    for item in rubric:
        item_id = item["id"]
        if item_id not in scores:
            problems.append(f"missing:{item_id}")
            continue
        score = scores[item_id]
        if isinstance(score, bool) or not isinstance(score, (int, float)):
            problems.append(f"out_of_range:{item_id}")
            continue
        if score < 0 or score > item["max"]:
            problems.append(f"out_of_range:{item_id}")
            continue
        total += score

    if problems:
        return None, problems

    claimed = draft.get("total")
    if claimed is not None and claimed != total:
        return None, ["total_mismatch"]
    return total, []


def _suspicious(source):
    text = source.casefold()
    return any(phrase in text for phrase in _GRADER_INSTRUCTIONS)
