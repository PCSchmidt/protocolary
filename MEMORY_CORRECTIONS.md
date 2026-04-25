# MEMORY_CORRECTIONS.md — Transcelerate | Reflexion Log
# New entries added ABOVE previous (newest first).
# Written at every gate close. Used to calibrate future estimates.

## REFLEXION LOG
# Format:
# ## REFLEXION: Gate N — [Gate Name]
# Date: [date]
# ESTIMATE: Predicted [X] hrs, Actual [X] hrs, Variance [+/-X]%
# WHAT WENT WRONG: [specific things that took longer or broke unexpectedly]
# WHAT WENT RIGHT: [approaches that worked better than expected]
# CORRECTION FOR FUTURE: [what to do differently next gate]
# MEMORY_SEMANTIC.md UPDATE: [pattern added/updated, or none]

[Empty — populated at first gate close]

## HISTORICAL LESSONS (pre-project)
# Key lessons from the original .NET POC attempt (April 2025) that inform this reboot.

### LESSON-001: Scope that is never confirmed is scope that expands infinitely
The original POC targeted "full StudyFlow SaaS platform" without ever writing a locked
spec. The result: extensive documentation, 936 bytes of Program.cs, and no working system.
**Correction:** SPEC.md is written and confirmed before any code. Scope changes require
an explicit spec update, not silent drift.

### LESSON-002: Tech stack chosen for the wrong reason causes friction that kills momentum
.NET was chosen because the TransCelerate reference implementation uses .NET. The developer's
primary language is Python. This mismatch created friction that contributed to the project
stalling.
**Correction:** Choose the stack the developer knows. The reference implementation is a
reading resource, not a dependency.

### LESSON-003: No target system selected = no integration testable
The original POC had no EDC system selected. Adapters were "initial structure only."
Without a real target system, there is no way to know if the transformation logic is correct.
**Correction:** Target system (REDCap) selected before Gate 1. Sandbox provisioned before
Gate 2 starts.

### LESSON-004: Mocked database tests pass while real integration fails
The original .NET approach planned mocked tests. The project's own notes document that
mocked tests passed while the production environment remained untested.
**Correction:** All tests use a real MongoDB instance via Docker Compose test profile.
No mocking of the database layer.
