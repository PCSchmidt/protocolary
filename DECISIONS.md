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
