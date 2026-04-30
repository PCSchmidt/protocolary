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
CONTEXT SAVE: 2026-04-30T12:00:00
Gate: Gate 3 — Adapter (PLANNED; BLOCKED on REDCap sandbox only)
Current phase: Active — Gate 1 CLOSED + CDISC API confirmed; only REDCap still pending

Gate status:
  - Gate 0 (Foundations): CLOSED — 2026-04-25, 4 hrs, 0% variance
  - Gate 1 (Schema): CLOSED — 2026-04-29, 4 hrs, 0% variance; 10 tests
  - Gate 2 (API): CLOSED — 2026-04-30, 4 hrs, -50% variance; 22 tests total
  - Gate 3 (Adapter): BLOCKED on REDCap sandbox (JHU ICTR — email sent)
  - Gate 4 (Demo): PLANNED

Completed since last save:
  - app/routes/studies.py: POST /studies, GET /studies, GET /studies/{id}, /arms, /concepts
  - main.py updated: router wired, /health upgraded to ping MongoDB
  - test_studies_api.py: 12 tests, all passing (22 total)
  - CDISC API fully investigated: portal key = docs only; data = members-only wall
  - Decision 008 revised: COSMOS data from GitHub, not live API
  - GOTCHA-007 logged; Gate 2 close protocol complete

Tests: 22/22 green
Run: docker compose --profile test up -d mongo_test && cd python && python -m pytest -v
Key: always use `python -m pytest` not bare `pytest`

KEY FINDINGS (do not forget):
  BiomedicalConcepts on StudyVersion.biomedicalConcepts — NOT StudyDesign
  usdm_model top-level = Wrapper (not StudyDefinition)
  uuid.UUID fields → str() before MongoDB; model_dump(mode='json') handles nested dict
  CDISC COSMOS data: public GitHub repo, not live API (members-only wall)
  API test pattern: monkeypatch connect/close/ensure_indexes as AsyncMock + override get_db
  FastAPI: HTTP_422_UNPROCESSABLE_CONTENT (not ENTITY — deprecated)

External blockers:
  - REDCap sandbox: awaiting JHU ICTR response (redcap@jhu.edu) — GATE 3 HARD DEPENDENCY
  - CDISC API data: members-only; using GitHub COSMOS repo instead (see Decision 008)

Decisions (all in DECISIONS.md):
  001 Python | 002 FastAPI | 003 MongoDB | 004 usdm pkg | 005 REDCap
  006 Streamlit | 007 MongoDB schema | 008 COSMOS from GitHub

Errors: ERR-001 UUID encoding | GOTCHA-007 CDISC members-only — see ERRORS.md

Next task when resuming:
  Gate 3 (Adapter) — BLOCKED on REDCap sandbox.
  When REDCap access confirmed:
    Step 1: Verify REDCap credentials (URL + API token) — note in DECISIONS.md
    Step 2: Write services/cdisc_seeder.py — fetch COSMOS YAML from GitHub, seed cdisc_cache
    Step 3: Write services/concept_mapper.py — USDM BC → REDCap field mapping table
    Step 4: Write services/redcap_adapter.py — generate REDCap Data Dictionary CSV
    Step 5: Implement GET /studies/{id}/redcap-export
    Step 6: Implement POST /studies/{id}/redcap-push
    Step 7: All tests green → type ADAPTER APPROVED
  While waiting for REDCap: schedule domain expert session (wife/medical writer)
  Approval word to close Gate 3: ADAPTER APPROVED
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
