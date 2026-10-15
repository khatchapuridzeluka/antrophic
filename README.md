# \# GradeMate

# 

# \*\*An AI grading assistant that helps university programming instructors grade Google Classroom code submissions: it fetches, unpacks and tests each one, then drafts rubric-based grades and feedback for the instructor to approve.\*\*

# CS6920 capstone · Fall 2026 · GradeMate · \[Name Surname], \[Name Surname], \[Name Surname], \[Name Surname]

# 

# > Status: Week 4 · spec v1, AGENTS.md and team rules in place; first slice (list and unpack submissions from a synthetic course) in progress.

# 

# \## The problem

# Programming instructors spend hours per assignment downloading each student's zip from Google Classroom, unpacking it, running the code, checking it against the rubric and writing feedback. Even when they use an AI chat to help, every step around it is manual, results are inconsistent, and nobody tracks each student's recurring mistakes.

# 

# \## Demo

# Coming later: 2-minute narrated video (YouTube Unlisted) · backup demo video (Week 14) · deployed URL (from Week 12)

# 

# \## Run it

# ```

# cp .env.example .env        # then fill in your own values

# pip install -r requirements.txt

# pytest -q

# ```

# The API (`uvicorn src.app:app --reload`) arrives with the first slices. All development data is synthetic: no real student work is ever stored in this repo.

# 

# \## How it works

# Planned pipeline: Google Classroom (fetch submissions) → unpack zips → run the instructor's tests in a sandbox (timeout, no network) → model drafts a rubric-based grade and feedback (via `src/llm.py`, which logs tokens, cost and latency) → instructor reviews and approves each grade → approved grades exported as CSV. Nothing is written back to Google Classroom.

# Architecture diagram: coming with the Design Review. Key decisions: \[docs/decisions/](docs/decisions/)

# 

# \## Does it work? (evidence)

# | What we measure | Result | Where |

# |---|---|---|

# | Unit tests | coming with the first slice | GitHub Actions |

# | Golden set | first run in Week 4 | evals/ |

# | Cost per graded submission | target < $0.02 | logs/usage.jsonl |

# | p95 latency per submission | target < 30 s | logs/usage.jsonl |

# 

# \## Case study

# Coming in Week 13: docs/case-study.md (what we built, what we delegated, what we measured, what we would change).

# 

# \## Team and how we work

# \[Name Surname] (repo keeper) · \[Name Surname] (spec keeper) · \[Name Surname] (eval keeper) · \[Name Surname] (feature lead)

# Team rules: \[docs/TEAM-REPO.md](docs/TEAM-REPO.md) · Spec: \[docs/spec.md](docs/spec.md) · Delegation log: \[docs/delegation-log.md](docs/delegation-log.md) · Journals: \[docs/journal/](docs/journal/) · Team contract: \[TEAM-CONTRACT.md](TEAM-CONTRACT.md)

