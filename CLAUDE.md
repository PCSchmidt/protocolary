# CLAUDE.md — Transcelerate Project Rules
# Load this file at every session start. It is the behavioral contract.

## Project Identity

**Name:** Transcelerate DDF Adapter POC
**Goal:** Prove that a USDM v4.x study definition can be automatically transformed into
a working REDCap EDC configuration.
**Stack:** FastAPI · Motor · MongoDB · `usdm` PyPI package · Docker Compose · Streamlit
**Phase:** POC (proof of concept) — scope discipline is the primary success factor.

## Files to Load at Every Session Start

Always load these five files before doing any work:

1. `CLAUDE.md` (this file)
2. `SPEC.md` — scope lock; check before accepting any task
3. `ERRORS.md` — check first before diagnosing any error
4. `MEMORY_SEMANTIC.md` — USDM domain knowledge and validated patterns
5. `PLANS.md` — current context save state and pending work

Load on demand when relevant:
- `DECISIONS.md` — when an architectural question arises
- `MEMORY_CORRECTIONS.md` — when estimating or choosing an approach
- `VERSION_ROADMAP.md` — when starting or closing a gate
- `TESTS.md` — when writing or reviewing tests
- `DEPLOYMENT_CONFIG.md` — when touching Docker or environment config
- `API_REGISTRY.md` — when adding or modifying endpoints
- `DEMO_CHECKS.md` — when working on the Streamlit dashboard

## The Five Gates

Gates advance only when the user types the exact approval word. No implicit advancement.
No skipping. No building two gates in parallel.

```
SCOPE CONFIRMED  →  SCHEMA APPROVED  →  API APPROVED  →  ADAPTER APPROVED  →  DEMO APPROVED
    Gate 0              Gate 1             Gate 2              Gate 3              Gate 4
```

| Gate | Approval Word | What It Means |
|---|---|---|
| 0 | `SCOPE CONFIRMED` | SPEC.md accepted, decisions logged, domain expert session complete |
| 1 | `SCHEMA APPROVED` | USDM object graph understood, sample fixture validated, MongoDB schema decided |
| 2 | `API APPROVED` | FastAPI ingestion layer passing all tests; POST/GET /studies /arms /concepts working |
| 3 | `ADAPTER APPROVED` | Offline adapter complete and tested, then imported successfully into a live REDCap project |
| 4 | `DEMO APPROVED` | Streamlit dashboard working; non-technical stakeholder completes workflow in <5 min |

## Gate Close Protocol (run at every gate close, in order)

1. Full pytest suite passes — no test count decrease from previous gate
2. `docker compose up` succeeds cleanly from a cold start
3. Run `/security` scan on any new endpoints
4. Run `DEMO_CHECKS.md` checklist if UI was changed
5. Update `VERSION_ROADMAP.md` — set gate Status=DONE, log actual hours
6. Append entry to `CHANGELOG.md`
7. Update `TESTS.md` with final test count and coverage
8. Write REFLEXION entry to `MEMORY_CORRECTIONS.md` (predicted vs actual hours; what was wrong)
9. Update `MEMORY_EPISODIC.md` with gate outcome row
10. Check `MEMORY_SEMANTIC.md` — add any validated patterns from this gate
11. Commit with tag: `git commit -m "gate-N-close: [Gate Name]" && git tag vN.N.N`

## Unbreakable Rules

- **Never write implementation code before `SCOPE CONFIRMED`**
- **Never advance a gate without the exact approval word typed by the user**
- **Never let the pytest count decrease between gates**
- **Never skip the REFLEXION entry at gate close**
- **Never build two gates in parallel**
- **Never use raw f-string queries against MongoDB — use Motor's typed query builders**
- **Never commit secrets, API keys, or `.env` files**
- **Never use `usdm` internal private APIs (underscore-prefixed) — only public interfaces**
- **Always run tests after any edit, before reporting the change as done**
- **Always read a file before editing it**

## Coding Standards

**Python:**
- Python 3.12+ with full type hints on all functions
- `ruff` for linting (run before committing)
- `black` for formatting
- No `Any` types — use specific Pydantic models or `usdm` package types
- Async all the way: FastAPI async routes, Motor async queries, no `asyncio.run()` in route handlers

**FastAPI:**
- All routes return typed Pydantic response models
- HTTP 422 for validation errors (FastAPI default — do not override)
- HTTP 404 for missing study IDs (not 500)
- All endpoints documented with `summary=` and `description=` parameters
- OpenAPI docs auto-generated; verify at `/docs` after adding any endpoint

**MongoDB / Motor:**
- Use `ObjectId` for `_id`; serialize to string in response models
- Index on `study_id` and `version` at minimum
- Never store raw USDM JSON as a flat blob — store the parsed object graph

**Tests:**
- Integration tests hit a real MongoDB instance (use Docker Compose test profile)
- No mocking of the database — lessons learned from the original POC failure mode
- Every new endpoint gets at least one happy-path and one error-path test
- Use a fixture corpus: the small synthetic fixture for fast unit tests plus version-pinned,
  provenance-recorded Protocol Explorer/TransCelerate examples for realistic integration tests
- Never assume `BiomedicalConcept.reference` is an NCI code; support COSMoS BC and Dataset
  Specialization URIs and use `code.standardCode.code` as a separate identity field

**Streamlit:**
- Streamlit app calls FastAPI via HTTP only — no direct DB access
- Separate `streamlit_app.py` from the FastAPI `app/` package entirely

## Context Management

- At 40% context: warn and save PLANS.md
- At 50% context: stop work, save state, commit, use `/clear`
- Never use `/compact` — it is lossy; always use `/clear`
- Before `/clear`, write a CONTEXT SAVE block to `PLANS.md`
- Gates estimated at 3+ hours should be split into sub-gates (e.g., Gate 2a, Gate 2b)

## Scope Discipline

Before accepting any task, check it against `SPEC.md`. If the task is out of scope, say so
explicitly and ask whether the user wants to update the spec before proceeding. Do not silently
expand scope. The original POC failed primarily because scope was never locked.

## Show Up as a Peer

Curious, honest about tradeoffs, willing to name bad ideas. Not a checklist bot. If an approach
is going to cause problems, say so before implementing it, not after. The goal is a working
REDCap adapter, not completed tasks.

## Gate 3 Execution Rule

Gate 3 is one formal gate with two execution phases:

- **Gate 3A — Offline Adapter:** realistic fixtures, concept identity normalization, pinned COSMoS
  metadata, domain-reviewed mappings, REDCap preview, and deterministic CSV export
- **Gate 3B — Live Verification:** REDCap client, metadata import, re-export comparison, and visual
  CRF review

Gate 3A may proceed without REDCap credentials. Gate 3B requires an API-enabled REDCap project.
The formal approval word remains `ADAPTER APPROVED` and is not given until both phases pass.
