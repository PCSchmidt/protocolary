# Transcelerate DDF Adapter POC

An independent proof-of-concept demonstrating that a USDM v4.x study definition can be
automatically transformed into a working REDCap EDC configuration.

> **Not an official TransCelerate project.** Independent adaptation under Apache 2.0.

---

## The One Question This POC Must Answer

> Can a USDM study definition be automatically transformed into a working EDC configuration?

---

## Current Status

| Gate | Name | Status |
|---|---|---|
| 0 | Foundations | ✅ CLOSED — 2026-04-25 |
| 1 | Schema | ⏳ PLANNED — ready to start |
| 2 | API | ⏳ PLANNED |
| 3 | Adapter | ⏳ PLANNED — blocked on REDCap sandbox + CDISC API key |
| 4 | Demo | ⏳ PLANNED |

**External blockers (Gates 1–2 unaffected):**
- REDCap sandbox: awaiting JHU ICTR response (`redcap@jhu.edu`)
- CDISC API key: request pending at cdisc.org

---

## Stack

| Layer | Technology |
|---|---|
| API | FastAPI (async) |
| Database | MongoDB via Motor (async) |
| USDM models | `usdm` PyPI package v0.67.0 |
| Demo UI | Streamlit |
| Deployment | Docker Compose (local only) |

The original .NET 6 skeleton is preserved in `POC_archive/` for reference.
All new development is in Python. See `DECISIONS.md` for rationale.

---

## Scope (POC only)

- **Source format:** USDM v4.x JSON
- **Target EDC:** REDCap (Phase 1 adapter only)
- **Study type:** Single-arm, vital signs assessments
- **BiomedicalConcept set:** Systolic BP, diastolic BP, heart rate, respiratory rate,
  temperature, height, weight, BMI
- **Deployment:** Local Docker Compose — no cloud, no auth, no multi-tenancy

Full scope lock is in `SPEC.md`.

---

## Getting Started (Gate 1 onward)

Prerequisites: Python 3.12+, Docker Desktop, `usdm` PyPI package.

```bash
# Gate 1 scaffold (not yet created — pending SCOPE CONFIRMED)
docker compose up
pytest
```

See `DEPLOYMENT_CONFIG.md` for full environment setup and `API_REGISTRY.md` for planned endpoints.

---

## Repository Map

| File / Folder | Purpose |
|---|---|
| `CLAUDE.md` | Behavioral contract — gates, rules, coding standards |
| `SPEC.md` | Scope lock — read before accepting any task |
| `DECISIONS.md` | Architecture decision log with rationale |
| `PLANS.md` | Context save state — read at every session start |
| `VERSION_ROADMAP.md` | Gate tracking with hour estimates |
| `CHANGELOG.md` | Milestone and gate-close log |
| `MEMORY_SEMANTIC.md` | USDM domain knowledge and validated patterns |
| `MEMORY_EPISODIC.md` | Session and gate history |
| `MEMORY_CORRECTIONS.md` | Reflexion log — predicted vs actual; lessons learned |
| `ERRORS.md` | Known failure modes and fixes |
| `TESTS.md` | Test strategy and registry |
| `DEPLOYMENT_CONFIG.md` | Docker Compose and environment configuration |
| `API_REGISTRY.md` | Planned FastAPI endpoint registry |
| `DEMO_CHECKS.md` | Streamlit demo verification checklist |
| `CONTEXT_BUDGET.md` | Context management rules |
| `Research/` | 5 background documents: feasibility, stack, business value, landscape, roadmap |
| `POC_archive/` | Original .NET 6 skeleton — preserved for reference, not active |

---

## Licensing

Based on TransCelerate DDF components licensed under Apache 2.0.
Independent adaptation — not affiliated with or endorsed by TransCelerate Biopharma Inc.
