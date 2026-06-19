# Architecture Decision Log

*Decisions are logged here with rationale. Knowing the why prevents relitigating settled questions
and helps evaluate edge cases when the rule doesn't obviously apply.*

---

## Decision 001 — Abandon .NET, Use Python

**Date:** April 2026
**Decision:** Rewrite the POC in Python. Do not extend the existing .NET 6 skeleton.

**Why:** The developer's primary language is Python. The original .NET choice was made because
the TransCelerate reference implementation uses .NET — a poor reason that adds friction without
adding value. The `usdm` PyPI package (v0.67.0) provides the full USDM data model in Python,
eliminating the only technical reason to stay in .NET. The existing .NET skeleton has 936 bytes
of Program.cs and no working functionality; there is nothing to preserve.

**How to apply:** All new code goes in the `python/` subdirectory. The old skeleton is preserved
in `POC_archive/` for reference only.

---

## Decision 002 — FastAPI over Flask or Django

**Date:** April 2026
**Decision:** Use FastAPI as the REST API framework.

**Why:** FastAPI is async-native (important for Motor/MongoDB and future Celery integration),
has automatic OpenAPI documentation, and is Pydantic-native — the same library the `usdm`
package uses for model validation. Flask would require adding async support; Django is too
heavy for a stateless transformation API.

**How to apply:** All API endpoints are FastAPI routes. No Flask or Django dependencies.

---

## Decision 003 — MongoDB over PostgreSQL

**Date:** April 2026
**Decision:** Use MongoDB (via Motor for async) as the primary datastore.

**Why:** USDM study definitions are deeply nested JSON documents. MongoDB's document model
stores them without schema friction. The original .NET POC also targeted MongoDB/CosmosDB,
so there is prior validation of this choice. A relational schema for USDM would require
significant ORM mapping work for no benefit at POC scale.

**How to apply:** Motor is the async MongoDB driver. SQLAlchemy is not used. If the project
eventually moves to a relational database (for reporting or multi-tenancy), that is a future
decision.

---

## Decision 004 — `usdm` PyPI Package over Hand-Rolled USDM Models

**Date:** April 2026
**Decision:** Use the official `usdm` PyPI package (v0.67.0, maintained by d4k/D Iberson-Hurst)
for all USDM model classes and serialization.

**Why:** The USDM object graph is large and complex. Building it from scratch would take weeks
and produce something less correct than the official implementation. The package is actively
maintained, tracks USDM standard versions, and integrates with the CDISC terminology API.

**Caveat:** The maintainer notes this was "not originally intended for public use" and formal
testing is ongoing. Pin the version (`usdm==0.67.0`) and do not upgrade without testing the
full transformation pipeline.

**How to apply:** All USDM model imports come from the `usdm` package. Do not define duplicate
USDM model classes.

---

## Decision 005 — REDCap as First Target EDC

**Date:** April 2026
**Decision:** Build the first downstream adapter for REDCap.

**Why:** REDCap has a public REST API, a free sandbox (sign up at projectredcap.org), and requires
no vendor NDA or procurement process. This eliminates the single biggest project risk from the
original POC: being blocked waiting for EDC sandbox access. REDCap is also widely used in
academic medical centers and smaller trials — a real market segment that is underserved by
enterprise EDC vendors.

**Tradeoff:** REDCap is not Medidata Rave or Veeva Vault. A REDCap demo does not prove that
the adapter pattern works for enterprise EDCs. It proves the core transformation logic works.
Enterprise EDC adapters are a Phase 2 decision.

**How to apply:** The adapter interface (`services/redcap_adapter.py`) should be designed as
an instance of a generic `EDCAdapter` abstract class so that future adapters (Medidata, Veeva)
implement the same interface without requiring API changes.

---

## Decision 006 — Streamlit for Demo UI (Not React/Angular)

**Date:** April 2026
**Decision:** Use Streamlit for the POC demonstration dashboard.

**Why:** Streamlit produces a working, professional-looking interactive UI in days, not weeks.
The original POC planned an Angular frontend — a significant scope addition for a solo developer
building a backend-first POC. The goal of the UI is stakeholder demonstration, not production UX.

**Tradeoff:** Streamlit is not suitable for production. If the project progresses beyond POC,
the UI layer will need to be replaced with React or another framework.

**How to apply:** The Streamlit app (`streamlit_app.py`) calls the FastAPI service via HTTP,
not directly to the database. This keeps the UI decoupled and the API testable independently.

---

## Decision 007 — MongoDB Document Schema for USDM Study Definitions

**Date:** April 2026 (Gate 1)
**Decision:** Store each USDM study definition as a single MongoDB document in the `studies`
collection, with extracted metadata fields at the top level and the full serialised object
graph nested under a `wrapper` key.

**Document shape:**
```
{
  "_id":                ObjectId   (MongoDB auto-generated)
  "study_id":           str        (wrapper.study.id — indexed)
  "study_name":         str        (wrapper.study.name)
  "version_identifier": str        (StudyVersion.versionIdentifier — compound indexed)
  "usdm_version":       str        (wrapper.usdmVersion)
  "created_at":         datetime
  "wrapper":            dict       (Wrapper.model_dump(mode='json') — nested dict, NOT a string)
}
```

**Indexes:**
- `study_id` (ascending)
- `(study_id, version_identifier)` (compound ascending)

**Why nested dict, not a flat JSON string blob:** MongoDB can address sub-fields in a nested
dict directly (e.g. `wrapper.study.versions.0.biomedicalConcepts`), enabling projection
queries that avoid deserialising the full graph. A string blob would require application-side
deserialisation for every query. This satisfies the CLAUDE.md rule: "Never store raw USDM
JSON as a flat blob — store the parsed object graph."

**Why top-level metadata fields:** Queries like "give me study X at version 2" should hit
an index, not scan the nested `wrapper` dict. Duplicating the four most-queried fields at
the top level makes this cheap.

**Tradeoff:** The `wrapper` dict is a snapshot at ingest time. If the USDM package model
changes between versions, old documents may not re-parse with the new package version without
a migration. This is acceptable at POC scale; add a schema version field if the project
progresses beyond Gate 4.

**How to apply:** See `app/models/study.py` for the Pydantic types. All writes to the
`studies` collection must follow this shape. Never write a JSON string to the `wrapper` field.

---

## Decision 008 — CDISC COSMOS Data Source: GitHub Static Files over Live API

**Date:** 2026-04-30 (updated after full API investigation)
**Decision:** Source CDISC COSMOS Biomedical Concept and Dataset Specialization data from the
**public GitHub repository** (`github.com/cdisc-org/COSMoS`), not the live CDISC Library API.
Select and pin an export/package for the POC; normal application startup and tests must use the
local snapshot rather than fetching the network.

**Why not the live API:** The CDISC Library API (`api.library.cdisc.org/api/cosmos/...`) requires
a paid CDISC organizational or individual membership to access COSMOS data. The developer portal
subscription (free account at `api.developer.library.cdisc.org`) grants documentation browsing
only — all actual data calls return `HTTP 401 "Members-only content"`. This was confirmed by:
- Direct API calls with `api-key` header (correct header name, confirmed via portal "Try it")
- The portal's own "Try it" feature also returning 401 with the same key
- Gateway URL confirmed: `https://api.library.cdisc.org/api/cosmos/v2/...`
- Auth header confirmed: `api-key: <subscription_key>`

**Why GitHub is sufficient for the POC:** The COSMoS repository publishes current Biomedical
Concept and Dataset Specialization exports, YAML, schemas, and supporting models. Content can be
versioned by commit/package, is reproducible, and requires no API credentials.

**Relevant COSMoS repository structure:**
```
export/                  # Current BC and Dataset Specialization CSV/Excel exports
yaml/
model/                   # LinkML and generated schemas/models
openapi/                 # COSMoS API definition
```

**How to apply at Gate 3:**
- Record the selected COSMoS commit and content license.
- Check in or explicitly refresh the minimal approved snapshot needed for the POC.
- Write `services/cosmos_provider.py` to resolve BC and Dataset Specialization identities by URI,
  NCI code, and specialization name.
- Tests read only the pinned local snapshot.
- A MongoDB cache is optional; it must not be populated through an implicit startup download.

**Future path to live API:** If the project scales beyond POC, a CDISC Individual Contributor
membership (~$500/yr) or institutional membership (via JHU) would unlock the live API.
The `api-key` header and `https://api.library.cdisc.org/api/cosmos/v2/` base URL are confirmed
correct — only the membership tier needs to change.

**CDISC_API_KEY in .env:** Keep as optional future configuration; it is not required by the Gate 3
build or test path.

**Gate 3A.2 pinned implementation:** Commit
`fc11c9dbdc12aae709653b45c4c9db7f58824cf5` is the immutable source for the POC snapshot. The
checked-in derived files contain only scoped vital-sign rows from the BC and SDTM Dataset
Specialization CSV exports. Their manifest records source URLs, Git blob hashes, SHA-256 hashes,
row counts, derivation, license, and attribution.

---

## Decision 009 — Protocol Explorer Fixture Corpus and Split Gate 3 Execution

**Date:** 2026-06-18

**Decision:** Use [Protocol Explorer](https://protocolexplorer.io/) as the discovery and download
source for realistic USDM integration fixtures, while retaining a small synthetic fixture for fast
unit tests. Execute Gate 3 in two phases: an offline adapter phase that begins immediately and a
live REDCap verification phase that begins when an API-enabled project is available.

**Why Protocol Explorer:** The public repository exposes structured USDM protocols together with
source metadata, original PDFs where available, and downloadable CDISC CORE conformance reports.
The examples include realistic schedule timelines, activities, repeated assessments, Biomedical
Concepts, and Dataset Specialization references that the current synthetic fixture does not model.

**Compatibility finding:** On 2026-06-18, nine public JSON files were inspected. Six parsed with
the project's pinned `usdm==0.67.0`; three failed model validation. The failing files are valuable
negative fixtures and demonstrate that a declared USDM 4.0 version is not sufficient evidence of
compatibility with one Python package release.

**Provenance caveat:** Many Protocol Explorer records currently point back to TransCelerate's
`ddf-sdr-api` sample-study repository. Protocol Explorer is therefore primarily an improved
discovery, visualization, validation, and download surface—not an independent canonical standard
source. Fixtures must retain source URL, download date, original filename, and attribution.

**Why split Gate 3:** REDCap credentials are not needed to implement or test concept resolution,
mapping decisions, REDCap row validation, preview output, or deterministic CSV generation.
Waiting for REDCap would unnecessarily block most of the valuable engineering work. Live REDCap
access remains mandatory before `ADAPTER APPROVED`.

**How to apply:**

- Gate 3A builds fixtures, concept identity normalization, an offline COSMoS provider, mapping
  tables, CSV generation, and preview/export endpoints.
- Gate 3B verifies the output through a live REDCap metadata import and visual CRF review.
- Use `https://github.com/cdisc-org/COSMoS`, not the obsolete
  `COSMoS-Biomedical-Concepts-and-Dataset-Specializations` repository name.
- Pin fixture files and COSMoS content by commit, package, or checked-in snapshot.
- Never make normal tests depend on Protocol Explorer, GitHub, or the CDISC API being online.
- Treat `BiomedicalConcept.reference`, `code.standardCode.code`, Dataset Specialization identity,
  and source activity as separate fields.

**Terms:** Protocol Explorer content is public and may be viewable or downloadable, but is supplied
by third parties for informational and standards-development purposes and is not independently
verified. Preserve provenance and do not treat the platform's technical conformance results as
clinical, regulatory, or scientific approval.

---

## Decision 010 — EDC-Neutral Intermediate Field Model

**Date:** 2026-06-19

**Decision:** Mapping logic produces governed, EDC-neutral `NeutralFieldDefinition` objects.
Target-specific formats such as REDCap Data Dictionary rows are produced later by adapters.

**Why:** Directly mapping USDM objects into REDCap CSV would spread REDCap assumptions through the
standards-processing core and make future Rave, Veeva, or Oracle adapters expensive. Clinical
meaning—datatype, unit, requiredness, validation intent, calculation, and source context—belongs in
a neutral model. Target-specific names and rendering types are optional hints.

**Governance:** The checked-in `poc-vital-signs` mapping library is versioned and tied to the pinned
COSMoS commit. Each mapping records status, rationale, and review items. Current mappings are
`needs_review`; technical implementation must not promote them to approved.

**How to apply:**

- Target adapters consume neutral fields and never parse raw USDM directly.
- Mapping libraries fail to load if specializations or BC IDs drift from pinned COSMoS.
- Duplicate mapping IDs, neutral field keys, and target variable names are rejected.
- Unmapped, ambiguous, standards-version fallback, and clinical-review states remain explicit.
- Mapping status becomes `mapped` only when governance status is `approved`.

---

## Decision 011 — Adopt Protocolary as the Independent Product Identity

**Date:** 2026-06-19

**Decision:** Rename the active project and product from the exploratory working name
“Transcelerate” to **Protocolary**. Use **Protocolary Build** for the initial protocol-to-EDC
product and POC. The domain `protocolary.com` has been secured.

**Why:** The former working name was confusingly close to TransCelerate BioPharma Inc., whose DDF
initiative and source materials are referenced by this project. A distinct identity reduces
customer confusion, search ambiguity, attribution risk, and potential trademark complications.
Protocolary is broad enough to support EDC build automation, review workflows, medical writing,
amendment impact, and future study intelligence without claiming those capabilities prematurely.

**Canonical technical names:**

- Brand: `Protocolary`
- Initial product: `Protocolary Build`
- Repository slug: `protocolary`
- Python distribution: `protocolary-core`
- API title: `Protocolary Clinical Study Compiler`
- Development database: `protocolary`
- Test database: `protocolary_test`

**How to apply:**

- Keep internal modules and domain types functional and brand-neutral.
- Rename active user-facing product references, package metadata, configuration defaults, and
  generated fixture metadata.
- Preserve TransCelerate BioPharma, DDF, repository URLs, licensing, and provenance references
  when they identify the independent organization or its materials.
- Preserve Git history and historical archive context; do not rewrite old commits.
- Rename the GitHub repository only after local changes pass tests and are committed.
- Treat domain ownership as distinct from formal trademark clearance.
