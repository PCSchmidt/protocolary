# TESTS.md — Transcelerate | Test Registry
# Updated at every gate close with final counts and coverage targets.
# Tests use real MongoDB via Docker Compose test profile — no mocking.

## TEST REGISTRY

| Gate | Unit | Integration | E2E | Total | Target | Status |
|---|---|---|---|---|---|---|
| Gate 0 — Foundations | 0 | 0 | 0 | 0 | 0 | DONE |
| Gate 1 — Schema | 8 | 2 | 0 | 10 | ≥ 5 | DONE |
| Gate 2 — API | 0 | 12 | 0 | 12 | ≥ 20 | DONE |
| Gate 3 — Adapter | — | — | — | — | ≥ 35 | PLANNED |
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

All test fixtures use real USDM JSON from TransCelerate GitHub examples, not hand-authored
synthetic data. Fixture files live in `python/tests/fixtures/`.

## COVERAGE TARGETS

- Integration tests: 100% of API endpoints
- Unit tests: 100% of transformation logic in `redcap_adapter.py` and `concept_mapper.py`
- No coverage target for `streamlit_app.py` (UI — covered by DEMO_CHECKS.md manual checklist)
