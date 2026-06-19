# MEMORY_SEMANTIC.md — Transcelerate | Persistent Domain Knowledge
# Updated at gate close when a pattern is validated or invalidated.
# Read at session start to restore domain context without re-researching.

## USDM DOMAIN KNOWLEDGE

### USDM Object Hierarchy (v4.x)
*Validated against usdm_model package v0.66.0 / v0.67.0 — Gate 1, 2026-04-29*
*Top-level container in usdm_model is `Wrapper`, not `StudyDefinition`.*
*⚠️ CORRECTION: BiomedicalConcepts live on StudyVersion, NOT StudyDesign (pre-Gate-1 diagram was wrong).*
```
Wrapper
  ├─ usdmVersion: str              (e.g. "4.0.0")
  ├─ systemName: Optional[str]
  └─ study: Study
        └─ versions: List[StudyVersion]
               ├─ versionIdentifier: str
               ├─ biomedicalConcepts: List[BiomedicalConcept]   ← HERE, not on StudyDesign
               │    ├─ name: str
               │    ├─ reference: str                           (NCI code string, e.g. "C49677")
               │    ├─ code: AliasCode
               │    │    └─ standardCode: Code
               │    │         ├─ code: str                      (e.g. "C49677")
               │    │         ├─ codeSystem: str                (e.g. "NCI")
               │    │         └─ decode: str                    (human label)
               │    └─ properties: List[BiomedicalConceptProperty]
               │         ├─ name: str                           (e.g. "result", "unit")
               │         ├─ datatype: str                       (integer, decimal, string, coded)
               │         ├─ isRequired: bool
               │         ├─ isEnabled: bool
               │         └─ responseCodes: List[ResponseCode]   (for coded properties)
               └─ studyDesigns: List[InterventionalStudyDesign | ObservationalStudyDesign]
                    ├─ arms: List[StudyArm]
                    ├─ epochs: List[StudyEpoch]
                    ├─ studyCells: List[StudyCell]              (arm × epoch grid)
                    ├─ activities: List[Activity]
                    └─ scheduleTimelines: List[ScheduleTimeline]
```

### BiomedicalConcept and Dataset Specialization Codes (Vital Signs POC Set)
Current identifiers validated against pinned COSMoS commit
`fc11c9dbdc12aae709653b45c4c9db7f58824cf5` — Gate 3A.2.

| Concept | Dataset Specialization | Current BC ID | Legacy synthetic reference | Notes |
|---|---|---|---|---|
| Systolic Blood Pressure | SYSBP | C25298 | C49677 | Legacy value collides with current Heart Rate |
| Diastolic Blood Pressure | DIABP | C25299 | C25299 | Current |
| Heart Rate | HR | C49677 | C49673 | Legacy value absent from pinned COSMoS |
| Respiratory Rate | RESP | C49678 | C49678 | Current |
| Body Temperature | TEMP | C174446 | C25206 | Legacy value absent from pinned COSMoS |
| Height | HEIGHT | C164634 | C25347 | C25347 remains a separate `Height` BC |
| Weight | WEIGHT | C81328 | C29463 | Legacy value absent from pinned COSMoS |
| BMI | BMI | C16358 | C16358 | Current |

Clinical ranges and REDCap field decisions remain Gate 3A.3 review items; COSMoS identifies
standard concepts and variables but does not authorize project-specific clinical validation limits.

### Biomedical Concept Identity in Real USDM Files
*Validated against Protocol Explorer public fixtures — 2026-06-18*

Do not treat `BiomedicalConcept.reference` as synonymous with an NCI code. Real USDM files may
use references such as:

```
/mdr/bc/packages/2025-04-01/biomedicalconcepts/C28421
/mdr/specializations/sdtm/packages/2025-04-01/datasetspecializations/SYSBP
```

The adapter must preserve these identity dimensions separately:

- `reference`: source URI or identifier from the USDM object
- `reference_type`: Biomedical Concept, Dataset Specialization, or unknown
- `standard_code`: `BiomedicalConcept.code.standardCode.code`
- `standard_code_system`: usually NCI, but never assume without reading the field
- `package_date` or source revision extracted from the URI/manifest
- concept properties
- source activity and schedule context

Repeated Dataset Specializations such as `SYSBP` may appear multiple times for different
activities, positions, or timepoints. Deduplicating only by NCI code would lose protocol meaning.

### Protocol Explorer
*Assessed 2026-06-18*

- Public repository: `https://protocolexplorer.io/`
- Operated by PA Consulting
- Browsing and per-protocol downloads are public
- Available artifacts can include USDM JSON, source PDF, and CDISC CORE reports in JSON/Excel
- Nine protocols were visible during assessment; six parsed with `usdm==0.67.0`, three did not
- Many records cite TransCelerate `ddf-sdr-api` sample studies as their source
- Content may be partial, third-party supplied, and unverified
- No documented public bulk API or OpenAPI endpoint was found during assessment

Use Protocol Explorer for realistic, provenance-recorded fixtures and compatibility tests. Do not
use it as a runtime dependency or as a substitute for REDCap validation.

### Current COSMoS Repository

The current official public repository is:

`https://github.com/cdisc-org/COSMoS`

The older recorded repository name,
`COSMoS-Biomedical-Concepts-and-Dataset-Specializations`, returns 404 and must not be used.
The current repository provides exports, YAML, schemas, models, and an OpenAPI definition. For
consumption, prefer the repository's `export` content or a deliberately selected YAML package.
Pin the revision/package and retain the CC BY 4.0 attribution for content.

### USDM Python Package Notes (`usdm` v0.67.0)
- Import root: `from usdm_model.study import Study`
- Requires `CDISC_API_KEY` env var for terminology lookups
- Excel import: `from usdm_excel import USDMExcel`
- JSON serialization: models use Pydantic v2 `.model_dump()` / `.model_validate()`
- Maintainer caveat: "originally not intended for public use; only informal testing performed"
- Pin version: `usdm==0.67.0` — do not upgrade without testing full pipeline

### REDCap Data Dictionary Format
REDCap instruments are configured via a CSV import called the Data Dictionary.
Key columns:
```
Variable / Field Name    — unique identifier (no spaces, max 26 chars)
Form Name               — instrument/form the field belongs to
Field Type              — text, notes, dropdown, radio, checkbox, calc, file
Field Label             — human-readable label shown to site staff
Choices (if dropdown)   — pipe-separated: 1, Option A | 2, Option B
Field Note              — instructional text below the field
Text Validation Type    — integer, number, date_mdy, etc.
Text Validation Min     — minimum valid value
Text Validation Max     — maximum valid value
Required Field          — y or blank
```

### REDCap API
- Base URL: `{redcap_url}/api/`
- Auth: token in POST body (`token=...`)
- Import instruments: `content=instrument`, `action=import`, `format=csv`
- Import records: `content=record`, `action=import`, `format=json`
- All requests are HTTP POST (even reads use POST with `action=export`)

## COMPETITIVE LANDSCAPE (key facts to avoid re-researching)

- ~25 organizations have publicly demonstrated DDF-compatible solutions (April 2026)
- USDM v4.0 released early 2025; stable; no major revision planned for 2026
- **Closest competitor:** CRScube (cubeCDMS) — USDM ingestion + EDC automation, but requires
  their own EDC system
- **Biggest free threat:** OpenStudyBuilder (Novo Nordisk, MIT/GPLv3) — upstream-focused
- **Market gap this project targets:** EDC-agnostic downstream adapter (USDM → any EDC)
- TransCelerate Solution Showcases: quarterly (September, December, March, July)
- DDF directory: https://transcelerate.github.io/ddf-directory/directory/directory.html

## VALIDATED PATTERNS
# Added at gate close when a pattern is confirmed by working code.
# Format: PAT-NNN: title | Confidence: LOW/MEDIUM/HIGH | Gate validated

PAT-001: Use synthetic fixtures for precise unit tests and pinned real-world fixtures for
compatibility/integration tests | Confidence: HIGH | Validated during Gate 3 planning

PAT-002: Separate USDM reference URI, specialization identity, standard code, and activity context
before mapping to an EDC field | Confidence: HIGH | Validated against Protocol Explorer fixtures

PAT-003: Reconstruct concept usage through
`BiomedicalConcept.id → Activity.biomedicalConceptIds → ScheduleTimeline.instances.activityIds`;
keep the grouped activity and scheduled-instance context in API output | Confidence: HIGH |
Validated in Gate 3A.1

PAT-004: Resolve real USDM concepts by Dataset Specialization URI first; treat NCI-only lookups as
potentially ambiguous because the same BC ID can identify both a BC and a specialization |
Confidence: HIGH | Validated in Gate 3A.2

PAT-005: When a fixture references an older COSMoS package, return current pinned metadata with an
explicit `fallback` version result; never claim an exact match | Confidence: HIGH |
Validated in Gate 3A.2

## INVALIDATED ASSUMPTIONS
# Record things that seemed true but turned out to be wrong.
# Prevents re-learning the same lesson.

- `BiomedicalConcept.reference` is always an NCI code — invalidated by real Protocol Explorer
  fixtures containing BC and Dataset Specialization URIs.
- The synthetic eight-vital-sign fixture is a real TransCelerate example — it is hand-authored and
  intentionally minimal.
- All USDM 4.0 JSON parses with `usdm==0.67.0` — three of nine assessed public files failed.
- A fixture named or presented as observational necessarily contains an
  `ObservationalStudyDesign` payload — the selected example currently parses as
  `InterventionalStudyDesign`.
- The original POC vital-sign code table is authoritative — several values are absent or identify
  different current COSMoS concepts.
