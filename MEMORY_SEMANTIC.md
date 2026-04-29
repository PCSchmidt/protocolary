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

### BiomedicalConcept CDISC Codes (Vital Signs POC Set)
Sourced from `POC_archive/src/SDR.Core.API/biomedical-concepts.json` and CDISC CT.

| Concept | CDISC Code | REDCap Field Type | Notes |
|---|---|---|---|
| Systolic Blood Pressure | C49677 | text / integer | mmHg; range 60-250 |
| Diastolic Blood Pressure | C25299 | text / integer | mmHg; range 40-150 |
| Heart Rate | C49673 | text / integer | bpm; range 30-250 |
| Respiratory Rate | C49678 | text / integer | breaths/min; range 8-60 |
| Body Temperature | C25206 | text / decimal | °C or °F; specify units |
| Height | C25347 | text / decimal | cm; range 50-250 |
| Weight | C29463 | text / decimal | kg; range 1-300 |
| BMI | C16358 | text / decimal | kg/m²; calculated field |
| Pain Assessment (NRS) | C38109 | text / integer | 0-10 scale |

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
- All requests are HTTP POST (even reads