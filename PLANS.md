# PLANS.md

Context save state for the Protocolary project. Written before `/clear` to preserve progress across context resets. Read at session resume to reconstruct state without re-reading the full conversation.

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
CONTEXT SAVE: 2026-06-19
Gate: Gate 3 — Adapter (Gate 3A IN PROGRESS; Gate 3B blocked on REDCap)
Current phase: Gate 3A.3 technical implementation complete; domain review pending

Gate status:
  - Gate 0 (Foundations): CLOSED — 2026-04-25, 4 hrs, 0% variance
  - Gate 1 (Schema): CLOSED — 2026-04-29, 4 hrs, 0% variance; 10 tests
  - Gate 2 (API): CLOSED — 2026-04-30, 4 hrs, -50% variance; 22 tests total
  - Gate 3A.1 (Fixture/Identity): COMPLETE — 31 tests total
  - Gate 3A.2 (COSMoS provider): COMPLETE — 50 tests total
  - Gate 3A.3 (Domain mapping): TECHNICAL COMPLETE — domain approval pending
  - Gate 3A.4 (Generator/API): PLANNED
  - Gate 3B (Live Verification): BLOCKED on API-enabled REDCap project
  - Gate 4 (Demo): PLANNED

Completed since last save:
  - Added PRODUCT_VISION, PRODUCT_ROADMAP, VALUE_METRICS, and TARGET_ARCHITECTURE
  - Added Decision 010: EDC-neutral intermediate field model
  - Added versioned poc-vital-signs mapping library tied to pinned COSMoS
  - Implemented neutral validation, calculation, target-hint, governance, and decision models
  - Implemented mapping by specialization, normalized name, current BC ID, and legacy code
  - Added explicit needs_review, mapped, unmapped, and ambiguous outcomes
  - Added fail-fast checks for COSMoS drift, duplicates, and target variable collisions
  - Drafted all eight scoped mappings without falsely approving clinical assumptions
  - Added VITAL_SIGNS_MAPPING_REVIEW.md for domain expert review
  - Full suite: 65/65 passing
  - Pinned COSMoS commit fc11c9dbdc12aae709653b45c4c9db7f58824cf5
  - Derived minimal CC BY 4.0 vital-sign snapshots from immutable BC and SDTM exports
  - Added source/blob/SHA-256 provenance and derived-file checksums
  - Implemented offline COSMoS provider with typed BC properties and SDTM variables
  - Added lookups by COSMoS URI, Dataset Specialization, and NCI code
  - Added explicit found/not_found/ambiguous and exact/fallback package results
  - Resolved all eight current vital-sign Dataset Specializations without network access
  - Identified stale synthetic mappings: current COSMoS uses C25298 SYSBP, C49677 HR,
    C174446 TEMP, C164634 HEIGHT, and C81328 WEIGHT
  - Full suite: 50/50 passing
  - Pinned three Protocol Explorer fixtures plus a provenance/checksum manifest
  - Added positive parser tests for CDISC Pilot and observational-named examples
  - Added expected validation-failure coverage for Allergan 3111-302-001
  - Added normalized concept identity service preserving reference type, specialization,
    package, standard code/version, properties, activity, timeline, and scheduled instances
  - Upgraded GET /studies/{id}/concepts without breaking direct-NCI synthetic fixtures
  - Confirmed the observational-named fixture currently parses as InterventionalStudyDesign;
    recorded rather than hiding the source/classification mismatch
  - Removed stale pytest `env` configuration; suite now runs without warnings
  - Full suite: 31/31 passing
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

Tests: 65/65 green
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
  010 EDC-neutral intermediate field model

Errors: ERR-001 UUID encoding | GOTCHA-007 CDISC members-only — see ERRORS.md

Next task when resuming:
  Gate 3A.3 domain review:
    Step 1: Review docs/product/VITAL_SIGNS_MAPPING_REVIEW.md with a qualified domain expert
    Step 2: Revise ranges, requiredness, units, BMI behavior, and repetition policy
    Step 3: Record reviewer/date/outcome and increment mapping library version
    Step 4: Promote only approved mappings from needs_review to approved
  Gate 3A.4 may begin in parallel only as a renderer of review-aware neutral fields; it must
  preserve needs_review warnings and cannot imply clinical approval.
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
