# 0003 · Ingest keeps only `.py` files

**Date:** Week 2 · **Decided by:** [names]

**Context.** AC2 says each submission is normalized to "source files", but never says which files count. Submissions arrive with images, READMEs, `__pycache__`, `node_modules` and virtual environments. Everything kept is later read by the model, so it costs tokens and adds noise, and binaries cannot be graded.

**Decision.** `src/unpack.py` copies only files ending in `.py`, from single files, folders and zips, and skips `__pycache__`, `node_modules`, `.venv`, `venv` and `.git`. A submission with no `.py` file is `unreadable` with reason `no_source_files`.

**Alternatives.** Keep every text file: includes READMEs that may explain the work, but also notes, logs and data files the rubric does not grade. Keep everything except a blocklist: simpler, but every new junk folder or binary type leaks through.

**Consequences.** Easier: small, predictable input to the model that fits the 6,000-token cap, and Python is the only language in scope (spec, Out of scope). Harder: a student's README or a required data file (for example `input.txt`) is not seen by the grader. Revisit when an assignment needs non-`.py` files or a second language is added.
