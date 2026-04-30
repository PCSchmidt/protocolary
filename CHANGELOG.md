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

## [v0.2.0] — 2026-04-30 | Gate 2: API — CLOSED

### Added
- `python/app/routes/__init__.py`
- `python/app/routes/studies.py` — 5 study endpoints: POST /studies, GET /studies,
  GET /studies/{id}, GET /studies/{id}/arms, GET /studies/{id}/concepts
- `python/tests/test_studies_api.py` — 12 API tests (happy path + error paths)
  using httpx AsyncClient + FastAPI ASGITransport + lifespan patching

### Changed
- `python/app/main.py` — wired studies router; upgraded /health to ping MongoDB
  and return `{"status": "ok", "db": "connected"}` or 503 if unreachable
- `python/app/config.py` — added `cdisc_base_url` setting
- `python/app/.env.example` — CDISC key status updated to confirmed/members-only
- `.gitignore` — added plain `.env` and `python/.env` entries
- `DECISIONS.md` — Decision 008 rewritten: GitHub static seeding over live CDISC API
- `ERRORS.md` — GOTCHA-007: CDISC developer portal key does not grant data access
- `VERSION_ROADMAP.md` — CDISC API confirmed; Gate 3 blocker now REDCap only

### Test counts: 22 total (10 Gate 1 + 12 Gate 2) — all passing

### Key Findings (Gate 2)
- CDISC developer portal subscription key grants documentation access only.
  Live COSMOS data at api.library.cdisc.org requires paid CDISC membership.
  Decision: seed COSMOS BC data from public GitHub repo at Gate 3.
- FastAPI `HTTP_422_UNPROCESSABLE_ENTITY` deprecated → use `HTTP_422_UNPROCESSABLE_CONTENT`.
- Lifespan patching pattern for API tests: monkeypatch connect/close/ensure_indexes
  as AsyncMocks, then override get_db with lambda returning test_db.

---

*Previous entries appear above.*
