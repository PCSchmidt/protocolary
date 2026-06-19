# Target Architecture

## Architectural Objective

Preserve the current POC as the standards-processing kernel of a future SaaS product without
introducing premature enterprise infrastructure.

## Core Transformation Flow

```text
USDM input
  → validated USDM object graph
  → normalized study and concept identity
  → pinned standards resolution
  → governed mapping decisions
  → EDC-neutral form specification
  → target adapter
  → generated artifact or target API
```

## EDC-Neutral Intermediate Model

Gate 3A.3 introduces the first neutral contract:

- `FormDefinition`
- `FieldDefinition`
- `ValidationRule`
- `ControlledValue`
- `MappingDecision`
- `SourceContext`
- `TargetHint`

The neutral model owns clinical meaning, datatype, unit, requiredness, validation intent, and
source provenance. A target hint may provide a preferred variable name or validation mapping, but
the neutral model must remain usable by future REDCap, Rave, Veeva, or Oracle adapters.

## Component Boundaries

| Component | Responsibility |
|---|---|
| USDM ingestion | Validate and persist versioned study definitions |
| Concept normalization | Preserve reference, code, package, activity, and schedule identity |
| Standards provider | Resolve immutable COSMoS metadata |
| Mapping library | Store governed sponsor/domain decisions |
| Mapping service | Produce neutral fields and explicit review outcomes |
| Target adapter | Render neutral definitions into target-system configuration |
| Transformation manifest | Record exact inputs, decisions, warnings, versions, and output hashes |

## Mapping Governance

Mappings are product data and should support:

- Stable identifier and schema version
- Applicable specialization and standard code
- Effective source versions
- Status: draft, reviewed, approved, retired
- Reviewer and review date
- Clinical rationale
- Sponsor or organizational scope
- Target hints separated from neutral field meaning
- Change history

The POC uses checked-in mappings. A future service may manage these records in a governed library.

## Future SaaS Data Boundaries

Potential future persistence:

- MongoDB or equivalent document storage for USDM versions
- Relational storage for organizations, users, permissions, workflows, and billing
- Object storage for protocols, reports, generated artifacts, and manifests

These are target boundaries, not current implementation requirements.

## Technical Evolution

- Migrate Motor to the PyMongo Async API before the persistence layer expands substantially.
- Add authentication, tenancy, and audit only when moving beyond the local POC.
- Prefer a modular monolith until independent scaling or ownership needs justify services.
- Keep network-based terminology services behind provider interfaces and pinned caches.

## Architecture Guardrails

- Target adapters never parse raw USDM directly.
- Mapping logic never emits target CSV rows directly.
- Clinical review state is never inferred from technical standards conformance.
- Version fallback, ambiguity, and unmapped states are visible in all downstream workflows.
- Generated artifacts are reproducible from immutable inputs.
