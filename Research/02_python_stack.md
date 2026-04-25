# Python Stack Recommendations

*Research conducted: April 2026*

## Why Abandon the .NET Stack

The original POC used .NET 6 because the TransCelerate reference implementation uses .NET 6.
This is a poor reason for a solo Python developer. The reference implementation is a reading
resource, not a dependency. The `usdm` PyPI package provides the USDM data model in Python,
eliminating the only technical reason to stay in .NET.

## Recommended Stack

| Component | Choice | Rationale |
|---|---|---|
| API framework | **FastAPI** | Async, automatic OpenAPI docs, Pydantic-native, excellent for REST APIs |
| USDM data model | **`usdm` (PyPI v0.67.0)** | Official CDISC/TransCelerate Python implementation, actively maintained |
| Validation | **Pydantic v2** | Already used by the `usdm` package; free schema validation |
| Database | **MongoDB + Motor** | Document-native storage; USDM JSON maps naturally to documents; matches original design intent |
| Async jobs | **Celery + Redis** | For transformation jobs that may be slow (large study definitions) |
| Deployment | **Docker Compose** | Consistent local dev; same compose file extends to production |
| Demo UI | **Streamlit** | Fast to build; excellent for pharma stakeholder demos without a React frontend |

## The `usdm` Package — The Key Unlock

```bash
pip install usdm
```

The package provides:
- Full USDM model class hierarchy (StudyDefinition, ClinicalStudy, StudyDesign, StudyArm,
  ScheduleTimeline, BiomedicalConcept, BiomedicalConceptProperty, etc.)
- Excel → USDM JSON import (useful for ingesting manually authored study definitions)
- JSON serialization/deserialization
- CDISC API integration for terminology lookup (requires `CDISC_API_KEY` env var)

Requires Python >=3.12.

**Caveat from the package maintainer:** "Originally not intended for public use" and "only informal
testing has been performed." Use it, but pin the version and test your own transformation logic
independently.

## Project Directory Structure

```
transcelerate/
  python/                        # New Python project root
    app/
      main.py                    # FastAPI app entry point
      routers/
        studies.py               # CRUD endpoints for study definitions
        transform.py             # Transformation/export endpoints
      models/
        usdm_wrappers.py         # Thin wrappers around usdm package models
      services/
        storage.py               # MongoDB read/write via Motor
        redcap_adapter.py        # USDM → REDCap transformation logic
        concept_mapper.py        # BiomedicalConcept → EDC field mapping
      data/
        biomedical-concepts.json # Salvaged from original POC
        concept_mappings.json    # USDM code → REDCap field mapping table (to build)
    tests/
      fixtures/
        sample_usdm.json         # Real USDM example JSON for tests
      test_api.py
      test_redcap_adapter.py
    streamlit_app.py             # Demo dashboard
    docker-compose.yml
    pyproject.toml
    .env.example
  Research/                      # This directory
  POC_archive/                   # Original .NET skeleton (preserved)
  SPEC.md
  DECISIONS.md
```

## Docker Compose Skeleton

```yaml
services:
  mongo:
    image: mongo:7
    ports:
      - "27017:27017"
    volumes:
      - mongo_data:/data/db

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  api:
    build: ./python
    ports:
      - "8000:8000"
    environment:
      - MONGO_URL=mongodb://mongo:27017
      - REDIS_URL=redis://redis:6379
      - CDISC_API_KEY=${CDISC_API_KEY}
    depends_on:
      - mongo
      - redis
    volumes:
      - ./python:/app

volumes:
  mongo_data:
```

## What to Install Immediately

```bash
pip install usdm==0.67.0
python -c "from usdm_model.study import Study; print('usdm package working')"
```

Then fetch a real USDM example JSON from the TransCelerate GitHub and run it through the
Excel import to see the full object graph before writing a single API endpoint.
