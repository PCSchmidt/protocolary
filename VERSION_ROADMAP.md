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
| v0.0 | **Foundations** | `SCOPE CONFIRMED` | Spec locked; decisions logged; domain expert session done; BiomedicalConcept mapping table drafted; REDCap sandbox provisioned | 4 | — | IN PROGRESS |
| v0.1 | **Schema** | `SCHEMA APPROVED` | USDM object graph explored via `usdm` package; real USDM fixture validated; MongoDB schema decided; test fixture committed | 4 | — | PLANNED |
| v0.2 | **API** | `API APPROVED` | FastAPI service running in Docker; POST /studies, GET /studies/{id}, /arms, /concepts all tested; `pytest` green | 8 | — | PLANNED |
| v0.3 | **Adapter** | `ADAPTER APPROVED` | USDM → REDCap Data Dictionary CSV transformation tested; push to live REDCap sandbox working; concept_mappings.json complete for vital signs set | 10 | — | PLANNED |
| v0.4 | **Demo** | `DEMO APPROVED` | Streamlit dashboard: Upload → Inspect → Map → Export; non-technical stakeholder completes workflow in <5 min | 6 | — | PLANNED |

**Total estimated:** 32 hours (part-time, ~4 hrs/week → ~8 weeks)

## CALIBRATION MULTIPLIER

No completed gates yet. Default multiplier: 1.0x.
Updated after Gate 0 close based on actual vs. estimated variance.

## POST-POC BACKLOG (out of scope for v0.x)

Items that are valid but explicitly deferred:
- Second EDC adapter (Medidata Rave or Veeva Vault — pending domain expert input)
- BiomedicalConcept library expansion (laboratory, safety assessments, PRO)
- Edit check / validation logic generation
- CRF Completion Guidelines document generation
- OpenStudyBuilder upstream integration
- Authentication / multi-tenancy
- Production cloud deployment
