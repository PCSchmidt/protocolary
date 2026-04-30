# API_REGISTRY.md — Transcelerate | Endpoint Registry
# Source of truth for what API endpoints exist, their gate, and test status.
# Update immediately when adding or modifying an endpoint.

## BASE URL

Local: `http://localhost:8000`
API docs: `http://localhost:8000/docs` (FastAPI auto-generated OpenAPI)

## ENDPOINT REGISTRY

### Studies — Core CRUD (Gate 2)

| Method | Path | Gate | Description | Tested |
|---|---|---|---|---|
| `POST` | `/studies` | 2 | Ingest a USDM JSON study definition | YES |
| `GET` | `/studies/{id}` | 2 | Retrieve a stored study definition | YES |
| `GET` | `/studies/{id}/arms` | 2 | List study arms (StudyArm objects) | YES |
| `GET` | `/studies/{id}/concepts` | 2 | List BiomedicalConcepts with CDISC codes | YES |
| `GET` | `/studies` | 2 | List all stored studies (id + name + version) | YES |

### Transformation — REDCap Adapter (Gate 3)

| Method | Path | Gate | Description | Tested |
|---|---|---|---|---|
| `GET` | `/studies/{id}/redcap-export` | 3 | Generate REDCap Data Dictionary CSV | NO |
| `POST` | `/studies/{id}/redcap-push` | 3 | Push generated instruments to REDCap API | NO |
| `GET` | `/studies/{id}/redcap-preview` | 3 | Preview mapping (USDM concept → REDCap field) as JSON | NO |

### Health (Gate 2)

| Method | Path | Gate | Description | Tested |
|---|---|---|---|---|
| `GET` | `/health` | 2 | Service health check (MongoDB connectivity) | YES |

## REQUEST / RESPONSE SHAPES
# Filled in as endpoints are implemented.

### POST /studies
```
Request body: USDM v4.x JSON (StudyDefinition root object)
Response 201: { "study_id": "...", "version": "...", "title": "..." }
Response 422: Pydantic validation error (malformed USDM)
```

### GET /studies/{id}/redcap-export
```
Response 200: Content-Type: text/csv
              Body: REDCap Data Dictionary CSV
Response 404: { "detail": "Study not found" }
Response 422: { "detail": "No BiomedicalConcepts in study match known mappings" }
```

## NOTES

- All responses are JSON except `/redcap-export` (CSV)
- Authentication: none in POC scope (see SPEC.md)
- Rate limiting: none in POC scope
- Versioning: no API versioning in POC scope (`/v1/` prefix is post-POC)
