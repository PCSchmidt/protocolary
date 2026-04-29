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
| v0.0 | **Foundations** | `SCOPE CONFIRMED` | Spec locked; decisions logged; domain expert session done; BiomedicalConcept mapping table drafted; REDCap sandbox provisioned | 4 | 4 | DONE |
| v0.1 | **Schema** | `SCHEMA APPROVED` | USDM object graph explored via `usdm` package; real USDM fixture validated; MongoDB schema decided; test fixture committed | 4 | 4 | DONE |
| v0.2 | **API** | `API APPROVED` | FastAPI service running in Docker; POST /studies, GET /studies/{id}, /arms, /concepts all tested; `pytest` green | 8 | — | PLANNED |
| v0.3 | **Adapter** | `ADAPTER APPROVED` | USDM → REDCap Data Dictionary CSV transformation tested; push to live REDCap sandbox working; concept_mappings.json complete for vital signs set | 10 | — | PLANNED ⚠️ BLOCKED pending REDCap sandbox (JHU ICTR) + CDISC API key |
| v0.4 | **Demo** | `DEMO APPROVED` | Streamlit dashboard: Upload → Inspect → Map → Export; non-technical stakeholder completes workflow in <5 min | 6 | — | PLANNED |

**Total estimated:** 32 hours (part-time, ~4 hrs/week → ~8 weeks)

## EXTERNAL DEPENDENCIES

| Dependency | Required By | Status | Action |
|---|---|---|---|
| REDCap sandbox (JHU ICTR) | Gate 3 | ⏳ Pending | Email sent to redcap@jhu.edu — awaiting response |
| CDISC API key | Gate 3 | ⏳ Pending | Submit account request at cdisc.org/cdisc-library/api-account-request |
| Domain expert session | Gate 3 pre-work | Deferred | 5 questions identified; schedule before Gate 3 starts |

Gates 1 and 2 have no external dependencies and can proceed immediately.

## CALIBRATION MULTIPLIER

Gate 0 actual = 4 hrs, estimate = 4 hrs, variance = 0%. M