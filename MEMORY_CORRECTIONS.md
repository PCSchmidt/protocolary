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

## REFLEXION: Gate 2 — API

Date: 2026-04-30
ESTIMATE: Predicted 8 hrs, Actual 4 hrs, Variance -50%
WHAT WENT WRONG: ~2 hrs spent investigating CDISC Library API access, discovering the developer
portal subscription key grants documentation access only — CDISC COSMOS data is members-only
behind a paid membership wall. Decision 008 was completely revised as a result.
WHAT WENT RIGHT: The actual API implementation was fast. Lifespan patching pattern
(monkeypatching connect/close/ensure_indexes as AsyncMocks) is clean and reusable. All 12 tests
passed on the first run. FastAPI dependency override, ASGITransport + AsyncClient, and MongoDB
projection queries all worked immediately with no debugging needed.
CORRECTION FOR FUTURE: Before building against any third-party API, run a single authenticated
data call first to confirm access tier. A 5-minute smoke test would have saved 2 hrs. For Gate 3:
confirm COSMOS GitHub data is accessible and inspect the YAML structure BEFORE writing the seeder.
MEMORY_SEMANTIC.md UPDATE: Added lifespan patching test pattern. No USDM hierarchy changes.

## REFLEXION: Gate 1 — Schema

Date: 2026-04-29
ESTIMATE: Predicted 4 hrs, Actual 4 hrs, Variance 0%
WHAT WENT WRONG: One pre-Gate-1 assumption in MEMORY_SEMANTIC.md was wrong: BiomedicalConcepts
are on StudyVersion (not StudyDesign). Discovered immediately on first package inspection —
no code was written against the wrong assumption. Also, usdm v0.67.0 requires Python >=3.12
so the sandbox (Python 3.10) cannot run the full test suite; the two async MongoDB tests
require Docker. All 8 non-DB assertions validated manually in the sandbox.
WHAT WENT RIGHT: The usdm_model package is cleaner than the maintainer caveat suggested.
Pydantic v2 model inspection made the full object graph legible in minutes. Round-trip
model_validate → model_dump works correctly. Fixture construction from the package was
straightforward once required fields were identified. The gate estimate was accurate.
CORRECTION FOR FUTURE: For Gate 2, spin up Docker test environment before writing tests, not
after, so pytest can run the full suite (including async DB tests) during development.
MEMORY_SEMANTIC.md UPDATE: Full corrected object hierarchy added, with validated field-level
detail (BiomedicalConcept.code is AliasCode → standardCode: Code; BiomedicalConcepts on
StudyVersion not StudyDesign; Wrapper is top-level not StudyDefinition).

## REFLEXION: Gate 0 — Foundations

Date: 2026-04-25
ESTIMATE: Predicted 4 hrs, Actual 4 hrs, Variance 0%
WHAT WENT WRONG: Domain expert session not completed before gate close (deferred to pre-Gate 3 — acceptable given she is not needed for schema/API work). REDCap sandbox not provisioned (waiting on JHU ICTR response — not blocking Gate 1).
WHAT WENT RIGHT: Harness setup faster than expected once Research/ documents were drafted. `usdm` package discovery eliminated hand-rolling models (saved estimated 8+ hrs). BiomedicalConcept mapping table drafted in MEMORY_SEMANTIC.md from POC_archive biomedical-concepts.json.
CORRECTION FOR FUTURE: Gate 0 criteria were slightly aspirational (REDCap sandbox + domain expert session). For planning-only gates with external dependencies, mark external blockers explicitly as "not blocking gate close" in SPEC.md upfront.
MEMORY_SEMANTIC.md UPDATE: None — Gate 0 is pre-code; no validated implementation patterns yet.

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
