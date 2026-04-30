# ERRORS.md — Transcelerate | Living Failure Log
# CHECK THIS FIRST before diagnosing any error.
# Format: ERR-NNN: title | root cause | fix | prevention

## KNOWN ERRORS

### ERR-001: UUID encoding failure when inserting usdm_model fields into MongoDB
**Symptom:** `ValueError: cannot encode native uuid.UUID with UuidRepresentation.UNSPECIFIED`
**Root cause:** Fields accessed directly from a usdm_model Pydantic object (e.g. `wrapper.study.id`)
are Python `uuid.UUID` objects. The default bson/Motor codec cannot encode them without an explicit
`UuidRepresentation` codec option. This affects any top-level document field set from a direct
model attribute reference.
**Fix:** Wrap with `str()` at the call site:
```python
# WRONG — crashes at insert_one
doc = {"study_id": wrapper.study.id, ...}

# CORRECT
doc = {"study_id": str(wrapper.study.id), ...}
```
`model_dump(mode="json")` handles this automatically inside the nested `wrapper` dict, but
**direct field access does not** — always use `str()` when writing uuid fields to MongoDB.
Also apply `str()` to the query predicate: `find_one({"study_id": str(wrapper.study.id)})`.
**Prevention:** All MongoDB insert/query code must use `str(obj.id)` for uuid fields.
Gate 2 API layer must follow this pattern in every route that handles study identifiers.
**First seen:** Gate 1 — 2026-04-29 | Fixed in `tests/test_usdm_fixture.py`

## STACK-SPECIFIC GOTCHAS
# Common failure modes for this stack, pre-seeded from experience.

### GOTCHA-001: Motor ObjectId not JSON serializable
**Symptom:** `TypeError: Object of type ObjectId is not JSON serializable`
**Root cause:** MongoDB `_id` is a `bson.ObjectId`; FastAPI's JSON encoder does not know it.
**Fix:** Add a custom encoder or use a response model that converts `_id` to `str`:
```python
class StudyResponse(BaseModel):
    id: str = Field(alias="_id")
    model_config = ConfigDict(populate_by_name=True)
```
**Prevention:** Always define Pydantic response models; never return raw Motor documents.

### GOTCHA-007: CDISC Library API requires paid membership — developer portal key does not grant data access
**Symptom:** `HTTP 401 {"message": "Members-only content. Visit https://www.cdisc.org/membership/rates-benefits for details."}`
**Root cause:** The CDISC developer portal at `api.developer.library.cdisc.org` issues subscription
keys that grant only documentation/portal access. The live COSMOS data at
`api.library.cdisc.org/api/cosmos/...` requires a paid CDISC membership (individual ~$500/yr
or institutional). Even the portal's own "Try it" feature returns 401 with the same key.
**Confirmed details:**
  - Correct URL base: `https://api.library.cdisc.org/api/cosmos/v2/`
  - Correct auth header: `api-key: <subscription_key>`
  - Auth works (no "missing key" error) but membership tier blocks data access
**Fix (for POC):** Use CDISC COSMOS GitHub repo instead. See Decision 008.
  All BC and Dataset Specialization YAML files are published publicly at:
  `github.com/cdisc-org/COSMoS-Biomedical-Concepts-and-Dataset-Specializations`
**Prevention:** Do not plan architecture around live CDISC API access without confirming
membership tier first. For POC, GitHub seeding is simpler and more reliable.
**First seen:** Gate 2 pre-work — 2026-04-30

### GOTCHA-002: `usdm` package requires CDISC_API_KEY even for local use
**Symptom:** `KeyError: 'CDISC_API_KEY'` or silent terminology lookup failure
**Root cause:** The `usdm` package calls the CDISC terminology API for code validation.
**Fix:** Set `CDISC_API_KEY` in `.env`; add to Docker Compose `environment:` block.
**Prevention:** `.env.example` documents this key; Docker Compose loads `.env` by default.

### GOTCHA-003: REDCap API returns 200 even on import errors
**Symptom:** `POST /api/` returns HTTP 200 but Data Dictionary not imported
**Root cause:** REDCap wraps errors in a JSON body with `error` key rather than HTTP 4xx.
**Fix:** Always check response body for `"error"` key after REDCap API calls.
**Prevention:** Wrap all REDCap API calls in a helper that raises on error body.

### GOTCHA-004: FastAPI async route calling synchronous Motor operation
**Symptom:** Route hangs or blocks the event loop
**Root cause:** `pymongo` (sync) used instead of `motor` (async) inside an `async def` route.
**Fix:** Use `motor.motor_asyncio.AsyncIOMotorClient`; all DB calls must be `await`-ed.
**Prevention:** DECISIONS.md Decision 002 — async all the way; no sync DB calls in routes.

### GOTCHA-005: `usdm` model validation fails on real TransCelerate example files
**Symptom:** `ValidationError` when parsing a USDM JSON fixture
**Root cause:** TransCelerate example files may be pinned to an older USDM version than
the installed `usdm` package.
**Fix:** Check the `usdmVersion` field in the fixture JSON; match to `usdm` package version.
**Prevention:** Pin `usdm==0.67.0` and use example files that match that version.

### GOTCHA-006: REDCap variable names over 26 characters rejected
**Symptom:** Import error: "Variable name exceeds 26 characters"
**Root cause:** REDCap enforces a 26-character limit on field variable names.
**Fix:** Truncate or abbreviate field names in the concept_mappings.json table.
**Prevention:** Add a validation step in `redcap_adapter.py` that raises on names > 26 chars.
