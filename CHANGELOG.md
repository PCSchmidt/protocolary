# CHANGELOG.md — Transcelerate
# Append entries at every gate close and significant milestone.
# Format: ## [version] — [date] | [Gate Name]

## [v0.0.0] — 2026-04-25 | Gate 0: Foundations — CLOSED

### Added
- Cloned repository from GitHub (dev branch)
- `Research/01_feasibility_analysis.md` — audit of original .NET POC; feasibility verdict
- `Research/02_python_stack.md` — Python stack recommendations and directory structure
- `Research/03_business_value.md` — 5-layer business value analysis for pharma/medical writing
- `Research/04_commercial_landscape.md` — competitive landscape; Tier 1/2/3 vendors; market gap
- `Research/05_poc_roadmap.md` — phased implementation roadmap with success criteria
- `SPEC.md` — scope lock for USDM v4.x → REDCap POC
- `DECISIONS.md` — 6 architecture decisions with rationale
- `CLAUDE.md` — behavioral rules, gates, unbreakable rules, coding standards
- `MEMORY_SEMANTIC.md` — USDM domain knowledge, BiomedicalConcept codes, REDCap format
- `MEMORY_EPISODIC.md` — session and gate log
- `MEMORY_CORRECTIONS.md` — reflexion log; pre-seeded with 4 lessons from original POC
- `PLANS.md` — context save state
- `VERSION_ROADMAP.md` — 5-gate roadmap with hour estimates
- `CONTEXT_BUDGET.md` — context management rules and save protocol
- `ERRORS.md` — failure log; pre-seeded with 6 stack-specific gotchas
- `TESTS.md` — test registry and strategy
- `DEPLOYMENT_CONFIG.md` — FastAPI/MongoDB/Docker Compose environment configuration
- `API_REGISTRY.md` — planned API endpoint registry
- `DEMO_CHECKS.md` — Streamlit demo verification checklist
- `CHANGELOG.md` (this file)

### Changed
- Renamed `POC/` → `POC_archive/` to preserve original .NET skeleton for reference

### Removed
- Nothing removed (original files preserved in `POC_archive/`)

---

## [v0.1.0] — 2026-04-29 | Gate 1: Schema — CLOSED

### Added
- `python/pyproject.toml` — Python 3.12+, pinned deps (fastapi, motor, usdm==0.67.0, pytest)
- `python/Dockerfile` — Python 3.12-slim image
- `python/.dockerignore`
- `python/.env.example` — all required environment variables with status notes
- `python/app/__init__.py`
- `python/app/main.py` — FastAPI skeleton with lifespan and `/health` endpoint
- `python/app/config.py` — pydantic-settings Settings class
- `python/app/database.py` — Motor async client, connect/close/ensure_indexes
- `python/app/models/__init__.py`
- `python/app/models/study.py` — StudySummary, StudyInDB, BiomedicalConceptSummary response models
- `python/tests/__init__.py`
- `python/tests/conftest.py` — Motor test client fixture; drops/recreates test collection per test
- `python/tests/fixtures/sample_study.json` — minimal valid USDM v4.0.0 fixture; 8 vital signs BCs
- `python/tests/test_usdm_fixture.py` — 10 tests (8 non-DB + 2 async MongoDB); all assertions validated
- `docker-compose.yml` — mongo (dev, port 27017), mongo_test (profile=test, port 27018), api service
- `DECISIONS.md` Decision 007 — MongoDB document schema for USDM study definitions

### Changed
- `MEMORY_SEMANTIC.md` — corrected USDM object hierarchy: BiomedicalConcepts are on
  StudyVersion (not StudyDesign); added validated field-level detail from package inspection
- `VERSION_ROADMAP.md` — Gate 1 marked DONE; calibration note added

### Key Finding (Gate 1)
The `usdm_model` package's top-level container is `Wrapper` (not `StudyDefinition`).
BiomedicalConcepts are stored on `StudyVersion.biomedicalConcepts`, not on `StudyDesign`.
This corrects a pre-Gate-1 assumption in MEMORY_SEMANTIC.md.

---

*Previous entries appear above.*
