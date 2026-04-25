# POC Implementation Roadmap

*Research conducted: April 2026*

## Governing Constraint

One developer, working part-time, building a POC whose single goal is to answer:

> **"Can a USDM study definition be automatically transformed into a working EDC configuration?"**

Everything in this roadmap is sized to that question, not to the "StudyFlow SaaS platform"
vision in the original strategy documents. Scope discipline is the primary lesson from the
first attempt.

## Phase 0 — Foundations (Days 1–3)

**This phase exists because the original attempt skipped it entirely.**

### 0a. Scope Lock (SPEC.md)

Write SPEC.md before any code is written. It must commit to exactly:
- USDM source format: USDM v4.x JSON
- Target EDC system: REDCap (public REST API, free sandbox, no procurement delay)
- Study type for demo: single-arm study with vital signs assessments
  (the existing `biomedical-concepts.json` covers this subset)
- Explicit out-of-scope: multi-tenancy, authentication, production deployment, other EDCs,
  protocol authoring, upstream USDM generation

### 0b. Architecture Decisions (DECISIONS.md)

Log every architectural decision before it becomes implicit. See DECISIONS.md.

### 0c. Domain Expert Session

Before writing transformation logic, conduct a working session with the project's medical
writing domain expert. Walk through a real CRF she has worked on and manually map its fields
to USDM BiomedicalConcepts. This reveals:
- Whether the USDM standard is rich enough to drive the EDC in practice
- Which BiomedicalConcept → EDC field mappings are mechanical vs. require judgment
- Where the standard has gaps that need workarounds
- Which EDC system to target after REDCap (based on real-world prevalence)

Output: a hand-drafted mapping table for vital signs (systolic BP, diastolic BP, heart rate,
respiratory rate, temperature, height, weight, BMI) → REDCap field definitions.

## Phase 1 — USDM Ingestion Layer (Weeks 1–2)

**Goal:** A running FastAPI service that accepts USDM JSON, validates it, stores it,
and retrieves it. Nothing more.

### Stack
```
Python 3.12+
FastAPI 0.11x
Motor (async MongoDB driver)
usdm==0.67.0
Pydantic v2
Docker Compose (MongoDB + API)
pytest + httpx (integration tests)
```

### Endpoints
- `POST /studies` — accepts USDM JSON body, validates against `usdm` package models,
  stores in MongoDB, returns a study ID
- `GET /studies/{id}` — retrieves a stored study definition
- `GET /studies/{id}/arms` — returns study design arms
- `GET /studies/{id}/concepts` — returns BiomedicalConcepts for the study

### Test Fixture
Use a real USDM example JSON from the TransCelerate GitHub, not a hand-authored fake.
TransCelerate publishes example files in the ddf-sdr-api repository.

### Success Criterion
`pytest` green. `curl -X POST /studies` with a real USDM document returns a stored study ID.
The full object graph (StudyDesign → StudyArm → ScheduleTimeline → BiomedicalConcept) is
retrievable.

## Phase 2 — REDCap Adapter (Weeks 3–5)

**Goal:** Given a stored USDM study definition, emit a REDCap-importable instrument
configuration. This is the hard, valuable part of the POC.

### Setup First
1. Sign up for a REDCap sandbox at https://projectredcap.org (or institutional instance)
2. Get a REDCap API token (1–2 days to provision)
3. Read the REDCap Data Dictionary import format (simple CSV structure)

### The Transformation

```
USDM StudyDesign
  └─ StudyArm
       └─ ScheduleTimeline
            └─ ScheduledActivityInstance
                 └─ BiomedicalConcept (e.g., "Blood Pressure" C49677)
                      └─ BiomedicalConceptProperty (systolic, diastolic, unit)
                           ↓
REDCap Data Dictionary row:
  variable_name, field_label, field_type, validation_type, choices
```

### The Hard Problem: CDISC Code → EDC Field Mapping

USDM BiomedicalConcepts are identified by CDISC codes (e.g., `C49677` for systolic blood
pressure). REDCap knows nothing about these codes. A mapping layer is required:

```json
{
  "C49677": {
    "redcap_variable": "sysbp",
    "redcap_label": "Systolic Blood Pressure",
    "redcap_type": "text",
    "redcap_validation": "number",
    "redcap_min": 60,
    "redcap_max": 250,
    "redcap_units": "mmHg"
  }
}
```

This JSON mapping table is one of the core IP artifacts of the entire project. Start with the
vital signs subset from `POC_archive/src/SDR.Core.API/biomedical-concepts.json` and extend
with the domain expert's input.

### Endpoints
- `GET /studies/{id}/redcap-export` — returns a REDCap Data Dictionary CSV
- `POST /studies/{id}/redcap-push` — pushes generated instruments to a REDCap project via API

### Success Criterion
A USDM study definition flows end-to-end to a live REDCap project with correct instrument
structure. The transformation is visible in REDCap's API playground. A non-technical stakeholder
can read the REDCap form and recognize the protocol's assessment structure.

## Phase 3 — Demo Dashboard (Week 6)

**Goal:** Something demonstrable to a pharma/CRO stakeholder that communicates the value
proposition without requiring them to read API documentation.

### Tech: Streamlit

Four screens:
1. **Upload** — paste or upload a USDM JSON file
2. **Inspect** — show parsed study arms, timelines, and BiomedicalConcepts in a readable table
3. **Map** — show the USDM → REDCap field mapping side by side (the "wow" screen)
4. **Export** — download the REDCap Data Dictionary CSV or push to a live REDCap sandbox

### Success Criterion
A person with a pharma background but no coding knowledge can upload a USDM file, see what
it contains, see how it maps to REDCap fields, and export or push the configuration — in under
5 minutes, without assistance.

## What Comes After (Not in Scope for This POC)

Once the REDCap adapter is working and demonstrated, evaluate:

1. **Second EDC adapter** — which EDC system is most prevalent in the domain expert's work?
   That determines the next adapter target (Medidata Rave, Veeva Vault EDC, or Oracle Clinical One).
2. **Upstream integration** — consuming USDM from OpenStudyBuilder or another upstream tool
   rather than manual JSON upload
3. **BiomedicalConcept library expansion** — beyond vital signs to laboratory, safety assessments,
   and patient-reported outcomes
4. **Edit check generation** — not just field structure but validation logic
5. **CRF Completion Guidelines generation** — document auto-generation from the same USDM source

These are Phase 2 of the product, not the POC. Do not scope them into Phase 0–3.
