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
CONTEXT SAVE: 2026-06-18T19:54:17-04:00
Gate: Gate 3 — Adapter (Gate 3A READY; Gate 3B blocked on REDCap)
Current phase: Documentation aligned; ready to build Gate 3A.1

Gate status:
  - Gate 0 (Foundations): CLOSED — 2026-04-25, 4 hrs, 0% variance
  - Gate 1 (Schema): CLOSED — 2026-04-29, 4 hrs, 0% variance; 10 tests
  - Gate 2 (API): CLOSED — 2026-04-30, 4 hrs, -50% variance; 22 tests total
  - Gate 3A (Offline Adapter): READY — no REDCap dependency
  - Gate 3B (Live Verification): BLOCKED on API-enabled REDCap project
  - Gate 4 (Demo): PLANNED

Completed since last save:
  - Full repository and roadmap review completed 2026-06-18
  - Current suite re-run against isolated MongoDB: 22/22 passing
  - Protocol Explorer assessed: public USDM repository with JSON/PDF/CORE report downloads
  - Nine public files inspected; six parse with pinned usdm==0.67.0 and three expose
    compatibility failures useful for negative tests
  - Real examples use BC and Dataset Specialization URIs in BiomedicalConcept.reference;
    current code's "reference = NCI code" assumption must be corrected
  - Current official COSMoS repository located at github.com/cdisc-org/COSMoS
  - Gate 3 split into 3A offline build and 3B live REDCap verification
  - Decision 009 added; roadmap, spec, tests, deployment, API registry, memories, and README aligned

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
  Protocol Explorer is a realistic fixture/discovery source, not a REDCap substitute
  Protocol Explorer currently exposes per-protocol downloads; no documented public API found
  Many Protocol Explorer records originate in TransCelerate ddf-sdr-api sample-studies
  Real BC reference values may be COSMoS URIs; standardCode is a separate field
  COSMoS current repo = https://github.com/cdisc-org/COSMoS

External blockers:
  - REDCap sandbox/project: awaiting JHU ICTR response — blocks Gate 3B only
  - Domain expert review: needed before finalizing the eight vital-sign mappings

Decisions (all in DECISIONS.md):
  001 Python | 002 FastAPI | 003 MongoDB | 004 usdm pkg | 005 REDCap
  006 Streamlit | 007 MongoDB schema | 008 COSMoS from GitHub
  009 Protocol Explorer fixtures + split Gate 3 execution

Errors: ERR-001 UUID encoding | GOTCHA-007 CDISC members-only — see ERRORS.md

Next task when resuming:
  Gate 3A.1 — Fixture and compatibility hardening:
    Step 1: Select and pin Protocol Explorer fixtures with provenance manifest
    Step 2: Keep synthetic fixture for fast unit tests; stop describing it as a real example
    Step 3: Add compatible-file and expected-validation-failure tests
    Step 4: Introduce normalized concept identity fields for reference URI/type,
            standard code, package version, properties, and source activity
    Step 5: Update GET /studies/{id}/concepts response without silently breaking identity
  Then Gate 3A.2:
    Build an offline COSMoS provider from a pinned cdisc-org/COSMoS export/package.
  REDCap credentials are not needed until Gate 3B.
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
