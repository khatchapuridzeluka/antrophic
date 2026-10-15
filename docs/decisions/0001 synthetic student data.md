# 0001 · Synthetic student data only

Date: Week 4 · Decided by: [names]

**Context.** GradeMate works on student submissions, grades and mistakes, which are personal data. The course rules forbid personal data, minors and sensitive data in the repo, and every graded milestone reads the repo.

**Decision.** All development, test and evaluation data is a synthetic course we write ourselves (students `s01`…`s30`), and live Google Classroom access uses only a test course the team creates.

**Alternatives.** Anonymized real submissions: still traceable from code style and comments, and needs consent. Real data kept outside the repo: easy to leak into logs, prompts or commits by accident.

**Consequences.** Easier: the repo can go public, tests are reproducible, and we can design submissions that hit every edge case on purpose (crash, infinite loop, empty zip, injection attempt). Harder: synthetic code may be cleaner than real student code, so golden-set results can look better than reality. We will watch for this and add messier cases as we find them.