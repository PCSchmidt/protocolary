# PLANS.md

Context save state for the Transcelerate project. Written before `/clear` to preserve progress across context resets. Read at session resume to reconstruct state without re-reading the full conversation.

## How to Use

Before `/clear`:

1. Update the LATEST CONTEXT SAVE section below
2. Commit: `git commit -m "wip: context save"`
3. Then `/clear`

At session start:

1. Load: CLAUDE.md, SPEC.md, ERRORS.md, MEMORY_SEMANTIC.md, PLANS.md
2. Read the LATEST CONTEXT SAVE block
3. Continue from "Next task"

## Latest Context Save

```text
CONTEXT SAVE: 2026-04-30T00:00:00
Gate: Gate 2 — API (PLANNED; ready to start NOW)
Current phase: Active — Gate 1 CLOSED + CDISC API confirmed; only REDCap still pending

Gate status:
  - Gate 0 (Foundations): CLOSED — 2026-04-25, 4 hrs actual, 0% variance
  - Gate 1 (Schema): CLOSED — 2026-04-29, 4 hrs actual, 0% variance; 10/10 tests green
  - Gate 2 (API): PLANNED — begin immediately; no external dependencies
  - Gate 3 (Adapter): BLOCKED on REDCap sandbox only (CDISC API NOW CONFIRMED)
  - Gate 4 (Demo): PLANNED

Completed since last save:
  - Fixed UUID encoding bug: all mongodb insert/query sites use str(wrapper.study.id)
  - 10/10 Gate 1 tests green (confirmed in Docker + venv on local machine)
  - ERR-001 logged in ERRORS.md (uuid.UUID must be wrapped with str() for MongoDB)
  - CDISC Library API access confirmed: api.developer.library.cdisc.org
  - Decision 008 logged: use v2 BC Endpoints + v2 Dataset Specialization endpoints
  - VERSION_ROADMAP, MEMORY_EPISODIC, DECISIONS.md all updated

Tests: 10/10 green
Run: docker compose --profile test up -d mongo_test && cd python && python -m pytest
Key: always use `python -m pytest` not bare `pytest` in this Git Bash + venv setup

KEY FINDINGS (do not forget):
  BiomedicalConcepts are on StudyVersion.biomedicalConcepts — NOT on StudyDesign
  usdm_model top-level container is Wrapper (not StudyDefinition)
  uuid.UUID fields from usdm_model must be wrapped with str() before MongoDB insertion
  CDISC API: v2 BC Endpoints are primary; v1 is deprecated
  See MEMORY_SEMANTIC.md for full corrected USDM hierarchy

External blockers:
  - REDCap sandbox: awaiting JHU ICTR response (email sent to redcap@jhu.edu)
  - CDISC API key: CONFIRMED 2026-04-30 — active at api.developer.library.cdisc.org

Decisions made (all logged in DECISIONS.md):
  001 Python over .NET | 002 FastAPI | 003 MongoDB | 004 usdm package
  005 REDCap as first EDC | 006 Streamlit UI | 007 MongoDB schema | 008 CDISC API v2

Errors encountered: ERR-001 (UUID encoding) — see ERRORS.md

Next task when resuming:
  Begin Gate 2 (API).
  Step 1: Add CDISC_API_KEY to python/.env and python/.env.example
  Step 2: Add cdisc_base_url to config.py Settings
  Step 3: Confirm key with smoke test — GET /mdr/bc/packages from CDISC Library API
  Step 4: docker compose --profile test up -d mongo_test
  Step 5: Implement POST /studies + tests
  Step 6: Implement GET /studies/{id} + tests
  Step 7: Implement GET /studies/{id}/arms + tests
  Step 8: Implement GET /studies/{id}/concepts + tests
  Step 9: All pytest green → type API APPROVED
  See API_REGISTRY.md for full endpoint shapes.
  Approval word to close Gate 2: API APPROVED
```

## Previous Saves

### Save: 2026-04-25T11:00:00 — Mid-Gate-0 (pre-approval)

```text
CONTEXT SAVE: 2026-04-25T11:00:00
Gate: Gate 0 — SCOPE CONFIRMED (not yet approved at time of save; subsequently closed)
Current phase: Harness complete; external access applications in flight

Completed this session:
  - Cloned repo from GitHub (dev branch)
  - Archived original .NET POC → POC_archive/
  - Created Research/ with 5 documents
  - Created SPEC.md and DECISIONS.md
  - Created full harness: CLAUDE.md, all MEMORY files, VERSION_ROADMAP.md,
    CONTEXT_BUDGET.md, ERRORS.md, TESTS.md, PLANS.md, DEPLOYMENT_CONFIG.md,
    API_REGISTRY.md, DEMO_CHECKS.md, CHANGELOG.md
  - Created .claude/hooks: block-dangerous, session-start, pre-compact
  - Researched REDCap and CDISC API access paths
  - Submitted REDCap membership application (email sent to redcap@jhu.edu)
```
