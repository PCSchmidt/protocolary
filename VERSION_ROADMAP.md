# VERSION_ROADMAP.md — Transcelerate | Gate Tracking
# Updated at every gate close. Actual hours logged at close.
# Build type: Exploratory/Prototype — target endpoint: Gate 4 DEMO APPROVED

## GOVERNANCE RULES

- No gate is skipped
- Failing tests = do not advance
- Gates estimated at 3+ hours must split into sub-gates (e.g., Gate 2a, Gate 2b)
- Variance > 30% at close triggers a REFLEXION entry in MEMORY_CORRECTIONS.md
- Scope changes require re-opening the current gate's approval, not silent expansion
- Out-of-scope requests are declined or deferred to a post-POC backlog

## GATE ROADMAP

| Version | Gate Name | Approval Word | Objective | Est Hrs | Act Hrs | Status |
|---|---|---|---|---|---|---|
| v0.0 | **Foundations** | `SCOPE CONFIRMED` | Spec locked; decisions logged; initial mapping drafted; external access and domain review explicitly deferred | 4 | 4 | DONE |
| v0.1 | **Schema** | `SCHEMA APPROVED` | USDM object graph explored via `usdm` package; synthetic fixture validated; MongoDB schema decided; test fixture committed | 4 | 4 | DONE |
| v0.2 | **API** | `API APPROVED` | FastAPI service running in Docker; POST /studies, GET /studies/{id}, /arms, /concepts all tested; `pytest` green | 8 | 4 | DONE |
| v0.3A | **Offline Adapter** | — | Protocol Explorer fixtures; normalized concept identity; pinned COSMoS provider; reviewed vital-sign mappings; REDCap preview + deterministic CSV export | 12 | — | IN PROGRESS — 3A.3 technical build done; review pending |
| v0.3B | **Live REDCap Verification** | `ADAPTER APPROVED` | Import generated dictionary into an API-enabled REDCap project; re-export and visually verify the resulting CRF | 3 | — | BLOCKED pending REDCap access |
| v0.4 | **Demo** | `DEMO APPROVED` | Streamlit dashboard: Upload → Inspect → Map → Export; non-technical stakeholder completes workflow in <5 min | 6 | — | PLANNED |

**Revised total estimated:** 37 hours. Completed: 12 hours. Remaining estimate: 25 hours.

## EXTERNAL DEPENDENCIES

| Dependency | Required By | Status | Action |
|---|---|---|---|
| Protocol Explorer | Gate 3A | ✅ Public | Nine downloadable protocols observed 2026-06-18; pin selected files and retain provenance |
| CDISC COSMoS GitHub | Gate 3A | ✅ Public | Current repository is `cdisc-org/COSMoS`; use pinned exports/YAML |
| Domain expert session | Gate 3A mapping review | Deferred | Review units, ranges, requiredness, BMI calculation, repeating visits, and instrument grouping |
| REDCap project + API token | Gate 3B only | ⏳ Pending | Continue JHU ICTR request; evaluate a temporary demonstration project if it permits API metadata import |

Gate 3A can proceed immediately. REDCap access blocks only Gate 3B and therefore does not prevent
building the transformation, preview, export, and automated test layers.

## GATE 3A SUB-GATES

| Sub-gate | Objective | Est Hrs | Status | Exit Condition |
|---|---|---:|---|---|
| 3A.1 | Fixture and compatibility hardening | 3 | DONE — 2026-06-19 | Three fixtures pinned; checksums, positive/negative compatibility, and normalized concept context tested |
| 3A.2 | COSMoS metadata provider | 3 | DONE — 2026-06-19 | Immutable commit and minimal snapshot pinned; URI/code/specialization resolution tested offline |
| 3A.3 | Domain mapping layer | 3 | TECHNICAL BUILD DONE — REVIEW PENDING | Eight mappings implemented; domain expert must approve or revise clinical assumptions |
| 3A.4 | REDCap generator and API | 3 | PLANNED | Deterministic CSV plus preview/export endpoints and golden-file tests |

## CALIBRATION MULTIPLIER

Gate 0 actual = 4 hrs, estimate = 4 hrs, variance = 0%. Multiplier: 1.0x.
Note: Gate 0 is planning-only (no code) — carry-forward value for coding gates is limited.

Gate 1 actual = 4 hrs, estimate = 4 hrs, variance = 0%.

Gate 2 actual = 4 hrs, estimate = 8 hrs, variance = -50% (faster than expected).
Key: lifespan patching pattern for API tests; CDISC API confirmed members-only (no data access);
Pinned GitHub data strategy adopted for Gate 3 COSMoS metadata.
Key finding: usdm_model package API is clean and well-structured. BiomedicalConcepts are on
StudyVersion (not StudyDesign as assumed pre-Gate-1) — MEMORY_SEMANTIC.md corrected.
Fixture round-trips cleanly. 8/8 non-DB test assertions validated.

## POST-POC BACKLOG (out of scope for v0.x)

Items that are valid but explicitly deferred:
- Second EDC adapter (Medidata Rave or Veeva Vault — pending domain expert input)
- BiomedicalConcept library expansion (laboratory, safety assessments, PRO)
- Edit check / validation logic generation
- CRF Completion Guidelines document generation
- OpenStudyBuilder upstream integration
- Authentication / multi-tenancy
- Production cloud deployment
