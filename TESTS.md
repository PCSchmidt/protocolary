# TESTS.md — Transcelerate | Test Registry
# Updated at every gate close with final counts and coverage targets.
# Tests use real MongoDB via Docker Compose test profile — no mocking.

## TEST REGISTRY

| Gate | Unit | Integration | E2E | Total | Target | Status |
|---|---|---|---|---|---|---|
| Gate 0 — Foundations | 0 | 0 | 0 | 0 | 0 | DONE |
| Gate 1 — Schema | 8 | 2 | 0 | 10 | ≥ 5 | DONE |
| Gate 2 — API | 0 | 12 | 0 | 12 | ≥ 20 | DONE |
| Gate 3A — Offline Adapter | — | — | — | — | 45–55 total | READY |
| Gate 3B — Live Verification | — | — | — | — | ≥ 2 optional live tests | BLOCKED |
| Gate 4 — Demo | — | — | — | — | ≥ 40 | PLANNED |

**Rule:** Test count must never decrease between gates.

## TEST STRATEGY

### What Gets Tested

**Unit tests** (`tests/unit/`):
- BiomedicalConcept → REDCap field mapping logic in isolation
- USDM object traversal helpers
- REDCap Data Dictionary CSV generation from sample concept data
- Variable name truncation / validation

**Integration tests** (`tests/integration/`):
- POST /studies with real USDM JSON fixture → 201 response + stored document
- GET /studies/{id} → returns correct study structure
- GET /studies/{id}/arms → returns correct arm list
- GET /studies/{id}/concepts → returns BiomedicalConcepts with CDISC codes
- GET /studies/{id}/redcap-export → returns valid CSV (validated against REDCap schema)
- POST /studies/{id}/redcap-push → pushes to REDCap sandbox (Gate 3+)

**E2E tests** (manual, logged in DEMO_CHECKS.md):
- Full Streamlit workflow: upload → inspect → map → export
- Non-technical user completes workflow in < 5 minutes

### What Is Not Mocked

Per DECISIONS.md (and MEMORY_CORRECTIONS.md LESSON-004): **MongoDB is never mocked.**
All integration tests use a real MongoDB instance via Docker Compose test profile.

```yaml
# In docker-compose.yml, test profile:
services:
  mongo-test:
    image: mongo:7
    ports:
      - "27018:27017"  # separate port from dev instance
    profiles: ["test"]
```

Run tests with: `docker compose --profile test up -d && pytest`

### Test Fixtures

Use a layered fixture corpus:

1. `sample_study.json` — the existing small, hand-authored synthetic fixture. Keep it for fast
   schema, storage, and endpoint tests. It contains eight scoped vital-sign concepts but no
   realistic activities or schedule timelines.
2. Protocol Explorer/TransCelerate examples — version-pinned realistic integration fixtures with
   a provenance manifest containing source URL, original filename, download date, checksum,
   declared USDM version, parser result, and usage notes.
3. Expected-incompatible examples — selected public files that currently fail
   `usdm==0.67.0` validation. Assert a controlled validation failure; do not silently mutate them
   into passing fixtures.

Normal tests must run offline. Network retrieval belongs in an explicit fixture-refresh command,
not in pytest setup.

Primary Gate 3A candidates:

- CDISC Pilot — complex interventional schedule and repeated vital-sign activities
- Observational example — alternate `StudyDesign` subtype
- One currently incompatible USDM 4.0 example — negative compatibility test
- Existing synthetic vital-sign fixture — precise eight-concept unit tests

## COVERAGE TARGETS

- Integration tests: 100% of API endpoints
- Unit tests: 100% of transformation logic in `redcap_adapter.py` and `concept_mapper.py`
- No coverage target for `streamlit_app.py` (UI — covered by DEMO_CHECKS.md manual checklist)
- Live REDCap tests use an explicit marker and credentials; they are excluded from routine CI
