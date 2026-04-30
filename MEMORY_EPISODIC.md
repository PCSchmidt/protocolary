# MEMORY_EPISODIC.md — Transcelerate | Session and Gate Log

Gate rows added at gate close. Stop events appended automatically.
Read at session start to reconstruct recent history.

## Gate Log

| Date       | Gate                 | Approval Word     | Outcome | Tests | Hours (Est → Act) | Notes                                                 |
|------------|----------------------|-------------------|---------|-------|-------------------|-------------------------------------------------------|
| 2026-04-25 | Gate 0 — Foundations | `SCOPE CONFIRMED` | CLOSED  | 0     | 4 → 4 hrs         | REDCap + domain expert session deferred; not blocking |
| 2026-04-29 | Gate 1 — Schema      | `SCHEMA APPROVED` | CLOSED  | 10    | 4 → 4 hrs         | Key finding: BiomedicalConcepts on StudyVersion not StudyDesign; MEMORY_SEMANTIC.md corrected |
| 2026-04-30 | Gate 2 — API         | `API APPROVED`    | CLOSED  | 22    | 8 → 4 hrs (-50%)  | 5 endpoints + health; lifespan patch pattern; CDISC members-only → GitHub seeding |

## Session Log

Format: `[Date] | Focus | Key decisions | Blockers | Next session start point`

### 2026-04-25 | Project reboot + harness setup + Gate 0 pre-work

- Reviewed original .NET POC (essentially documentation + 936-byte skeleton)
- Decided to reboot in Python; archived .NET POC as POC_archive/
- Established Python stack: FastAPI + Motor + MongoDB + usdm + Docker + Streamlit
- Identified market gap: downstream USDM → EDC adapter; REDCap first target
- Created Research/ (5 documents), SPEC.md, DECISIONS.md
- Created full harness: CLAUDE.md, all MEMORY files, VERSION_ROADMAP.md, etc.
- Researched REDCap access: individual license does not exist; JHU institutional
  access via ICTR is likely path; emailed `redcap@jhu.edu` and submitted membership
  application describing POC objectives — awaiting response
- Researched CDISC API: transitioning to member-only benefit in 2026; Individual
  Contributor membership $500/yr; JHU institutional membership likely exists;
  CDISC API not required until Gate 3 (usdm package works without it for model ops)
- Domain expert session (wife/medical writer): deferred — not blocking Gate 0;
  5 key questions identified; needed before Gate 3 adapter work
- Next: CDISC API account request submission → SCOPE CONFIRMED → Gate 1 scaffold

### 2026-04-29 | Repo cleanup + consolidation while waiting on API access

- Context: Both REDCap (JHU ICTR) and CDISC API access requests are pending externally
- No coding work possible yet; used session to clean and consolidate the repo
- Deleted 4 stale pre-reboot artifacts from root:
    PROJECT_NOTES.md / .pdf (April 2025 empty .NET-era exploration template)
    POC_STRATEGY.md / .pdf (.NET 6/Azure/Angular strategy — superseded by DECISIONS.md + SPEC.md)
- Refreshed PLANS.md context save to reflect Gate 0 CLOSED and accurate blocker status
- Updated VERSION_ROADMAP.md to flag REDCap sandbox as Gate 3 hard dependency
- Updated README.md to reflect Python reboot and current gate status
- No architectural decisions changed; no scope changes; harness intact
- Blockers: REDCap sandbox (Gate 3), CDISC API key (Gate 3) — both pending external orgs
- Gate 1 (Schema) has no external dependencies and can begin as soon as SCOPE CONFIRMED is typed
- Next session start point: type SCOPE CONFIRMED → Gate 1 Python scaffold

### 2026-04-30 | Gate 2 — API work

- Wrote app/routes/studies.py: POST /studies, GET /studies, GET /studies/{id}, /arms, /concepts
- Updated main.py: wired router, upgraded /health to ping MongoDB
- Wrote 12 API tests in test_studies_api.py using httpx AsyncClient + ASGITransport
- Key pattern: monkeypatch connect/close/ensure_indexes as AsyncMock; override get_db with test_db
- 22/22 tests passing; fixed HTTP_422_UNPROCESSABLE_ENTITY → HTTP_422_UNPROCESSABLE_CONTENT deprecation
- Gate 2 closed in 4 hrs (estimate was 8 hrs — CDISC investigation took time but API work was fast)
- Gate 3 still blocked on REDCap; COSMOS data will be seeded from GitHub

### 2026-04-30 | CDISC API access confirmed + Gate 1 final fix

- CDISC Library API access confirmed active at api.developer.library.cdisc.org
- 5 endpoints available: CDISC Library API (base), v1/v2 BC Endpoints, v1/v2 Dataset Specialization Endpoints
- Decision 008 logged: v2 BC Endpoints + v2 Dataset Specialization are primary targets; v1 deprecated
- Gate 3 now BLOCKED on REDCap only (CDISC was the second blocker — now cleared)
- Fixed final UUID encoding bug in Gate 1 tests: all uuid field references now use str() in MongoDB ops
- All 10 Gate 1 tests green; ERR-001 logged in ERRORS.md
- Next: begin Gate 2 — add CDISC_API_KEY to .env, smoke-test key, then build study CRUD endpoints

### 2026-04-29 | Gate 1 — Schema work

- Explored usdm_model package API via sandbox (Python 3.10 / usdm 0.66.0 — close enough to 0.67.0)
- Discovered key correction: BiomedicalConcepts live on StudyVersion, not StudyDesign
- Built minimal USDM v4.0.0 fixture programmatically; 8 vital signs BCs round-trip cleanly
- Created full Python project scaffold: pyproject.toml, Dockerfile, docker-compose.yml,
  FastAPI app skeleton (health endpoint only), config.py, database.py, study models
- Wrote 10-test suite (8 non-DB + 2 async MongoDB); all 8 non-DB assertions validated in sandbox
- Logged Decision 007 (MongoDB document schema) in DECISIONS.md
- Corrected and expanded USDM object hierarchy in MEMORY_SEMANTIC.md
- Gate 1 close protocol complete: VERSION_ROADMAP, CHANGELOG, TESTS.md, MEMORY_CORRECTIONS,
  MEMORY_EPISODIC all updated
- User shared TransCelerate GitHub repo URLs — noted for Gate 2 fixture sourcing
- Note: async MongoDB tests require Docker (`docker compose --profile test up -d mongo_test`)
- Next session start: Gate 2 — FastAPI study endpoints; spin up Docker first

## Stop Events

Appended by hooks when session ends or `/clear` is called.
Format: `[timestamp] | reason | gate | tests passing | context %`

[Empty — populated automatically]
