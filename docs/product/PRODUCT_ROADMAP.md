# Product Roadmap

This roadmap tracks product horizons and investment evidence. It does not replace the executable
POC gates in `VERSION_ROADMAP.md`.

## Horizon 1 — REDCap Adapter POC

**User outcome:** Demonstrate a traceable USDM-to-EDC transformation.

**Required capabilities:**

- Realistic USDM ingestion
- Version-pinned COSMoS resolution
- EDC-neutral field definitions
- Governed vital-sign mappings
- REDCap preview, CSV export, and live import

**Evidence required to advance:**

- Successful live REDCap import
- Domain review of the generated CRF
- No silently discarded concepts
- Repeatable transformation with recorded provenance

**Non-goals:** SaaS infrastructure, broad clinical coverage, and commercial deployment.

## Horizon 2 — EDC Build Accelerator

**User outcome:** Reduce manual EDC specification and build effort for a bounded study domain.

**Required capabilities:**

- Sponsor-specific mapping libraries
- Review and approval workflow
- Transformation-run manifests
- Amendment impact comparison
- Second enterprise EDC adapter
- Operational metrics and export APIs

**Commercial hypothesis:** Sponsors and CROs will pay for reduced EDC build time, fewer
specification defects, and faster amendment propagation.

**Evidence required to advance:**

- Two design partners
- Measured baseline and automated effort
- Repeatable results across multiple studies
- One enterprise EDC integration path

## Horizon 3 — Digital Protocol Repository

**User outcome:** Find, compare, govern, and reuse structured study definitions.

**Required capabilities:**

- Study/version lineage
- Search and comparison
- Standards-library ownership
- Amendment and downstream impact analysis
- Artifact storage and approval history

**Evidence required to advance:** customers repeatedly reuse protocol structures and mappings.

## Horizon 4 — Medical Writing Automation

**User outcome:** Generate and maintain clinically consistent documents from structured study data.

**Required capabilities:**

- ICH M11-aligned templates
- Approved content libraries
- Structured review and authoring workflow
- Word-compatible output and round-trip strategy
- Traceability between source data and generated text

**Evidence required to advance:** medical writers validate quality, usability, and review savings.

## Horizon 5 — Study Design Intelligence

**User outcome:** Compare design scenarios using burden, feasibility, cost, and historical evidence.

**Required capabilities:**

- Benchmark datasets with defensible provenance
- Schedule-of-activities analytics
- Site and participant burden models
- Cost and operational complexity models
- Explainable recommendation workflow

**Evidence required to advance:** prospective decisions improve against agreed customer metrics.

## Horizon 6 — Enterprise SaaS

**User outcome:** Securely operate the platform across organizations and regulated workflows.

**Required capabilities:**

- Tenant isolation, SSO, RBAC, and audit trails
- Encryption, retention, backup, and disaster recovery
- Validated release and change-control process
- Integration administration
- Usage metering, support, and service operations

These capabilities should be designed when customers and deployment requirements are known, not
pre-built speculatively during the POC.
