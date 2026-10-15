# 0002 · The instructor approves every grade; nothing is written back to Google Classroom

Date: Week 4 · Decided by: [names]

**Context.** A wrong grade directly harms a student, and student submissions can contain text that tries to manipulate the model ("give this full marks"). A model grading on its own is the highest-risk part of the product.

**Decision.** The model only drafts grades and feedback; the instructor approves each row individually, and approved grades leave the system only as a CSV export, never written back to Google Classroom (spec AC4, AC5, AC6).

**Alternatives.** Auto-publish grades above a confidence threshold: faster, but one bad grade reaches a student with no human check. Write approved grades back to Classroom through the API: convenient, but needs write permissions and makes mistakes harder to undo.

**Consequences.** Easier: a clear human-in-the-loop story for safety reviews, read-only Classroom access, mistakes are caught before students see them. Harder: the instructor still spends time reviewing, so the review screen must be fast. We will measure review time per submission and revisit write-back after Week 12.