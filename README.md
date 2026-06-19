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
| 1 | Schema | ✅ CLOSED — 2026-04-29 |
| 2 | API | ✅ CLOSED — 2026-04-30; 22 tests passing |
| 3A | Offline Adapter | 🚧 IN PROGRESS — mapping layer implemented; domain review pending |
| 3B | Live REDCap Verification | ⏳ BLOCKED — awaiting API-enabled REDCap project |
| 4 | Demo | ⏳ PLANNED |

Gate 3 is no longer treated as wholly blocked. Protocol Explorer and the public CDISC COSMoS
repository provide enough realistic USDM and standards metadata to build and test the offline
adapter now. REDCap access is required only for the final live import verification.

**Current external dependency:**
- API-enabled REDCap project: awaiting JHU ICTR response (`redcap@jhu.edu`)

**Current public data sources:**
- [Protocol Explorer](https://protocolexplorer.io/) — downloadable real-world USDM protocols,
  source documents, and CDISC CORE conformance reports
- [CDISC COSMoS](https://github.com/cdisc-org/COSMoS) — Biomedical Concepts and Dataset
  Specializations; use version-pinned exports/YAML rather than the paid live API

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

## Getting Started

Prerequisites: Python 3.12+, Docker Desktop, `usdm` PyPI package.

```bash
# Start the isolated test database
docker compose --profile test up -d mongo_test

# Run the current 65-test suite
cd python
python -m pytest -v
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
| `docs/product/` | Product vision, commercial roadmap, value metrics, and mapping review |
| `docs/architecture/` | Target architecture and SaaS evolution guardrails |
| `POC_archive/` | Original .NET 6 skeleton — preserved for reference, not active |

---

## Licensing

Based on TransCelerate DDF components licensed under Apache 2.0.
Independent adaptation — not affiliated with or endorsed by TransCelerate Biopharma Inc.
