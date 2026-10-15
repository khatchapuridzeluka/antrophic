# Fake course · assignment `a01`

Synthetic data only (decision 0001). Names and emails in `roster.json` are fake and must never leave `list_submissions`. The tests and any demo use exactly these files.

| Student | State | Attachments | Expected `ingest` |
|---|---|---|---|
| s01 | TURNED_IN | `solution.py` | ok · `solution.py` |
| s02 | TURNED_IN | folder `project/` with `main.py`, `utils.py`, `node_modules/`, `diagram.png` | ok · only `main.py`, `utils.py` |
| s03 | LATE | `hw.zip`: `pkg/a.py`, `pkg/notes.txt` | ok · `pkg/a.py` |
| s04 | TURNED_IN | `broken.zip`, really a text file | unreadable · `corrupt_archive` |
| s05 | TURNED_IN | none | unreadable · `empty` |
| s06 | TURNED_IN | `README.md`, `screenshot.png` | unreadable · `no_source_files` |
| s07 | no folder | none | missing |
| s08 | TURNED_IN | `evil.zip`: `ok.py`, `../escape.py` | unreadable · `unsafe_archive`, nothing extracted |

List a zip without extracting it: `python -m zipfile -l <path>`.
