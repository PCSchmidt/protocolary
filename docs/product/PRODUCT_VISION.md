# Product Vision

## Purpose

Transcelerate is intended to become an API-first clinical-development automation platform that
reduces the manual re-entry, reconciliation, and document maintenance required to move a study
from protocol design into operational systems.

The current proof of concept remains deliberately narrower: prove that a structured USDM study
definition can produce a correct REDCap configuration. This document describes the destination,
not an authorization to expand the active POC scope.

## Customer Problem

Pharmaceutical sponsors and CROs repeatedly translate the same study intent across:

- Protocol documents
- Schedules of activities
- EDC builds
- Study-startup specifications
- Medical-writing deliverables
- Amendments and downstream change assessments

These translations are often manual, slow, inconsistent, and difficult to audit. The commercial
opportunity is to preserve study intent as structured, governed data and generate downstream
artifacts from it.

## Initial Commercial Wedge

The first product is an **EDC Build Accelerator**:

1. Ingest a USDM study definition.
2. Resolve standards metadata and sponsor mappings.
3. Expose every automated decision and unresolved item for review.
4. Generate target-system configuration.
5. retain a reproducible transformation manifest.

REDCap proves the adapter pattern. It is not the intended limit of the product.

## Long-Term Product Direction

1. **EDC Build Accelerator** — governed study-to-EDC automation.
2. **Digital Protocol Repository** — versioning, comparison, lineage, and amendment impact.
3. **Medical Writing Automation** — ICH M11-aligned document generation and reusable content.
4. **Study Design Intelligence** — burden, feasibility, cost, and design scenario analysis.
5. **Enterprise SaaS Platform** — secure multi-organization workflows and integrations.

## Positioning

Directionally, platforms such as Faro Health validate demand for structured study design,
connected authoring, and workflow automation. Transcelerate should differentiate through:

- Open standards and transparent transformations
- EDC-neutral architecture
- API-first integration
- Explicit provenance and human-review boundaries
- Modular adoption rather than an all-or-nothing platform replacement

## Product Principles

- **Structured source of truth:** preserve USDM and its version history.
- **Vendor neutrality:** target-specific adapters consume a neutral intermediate model.
- **No silent loss:** unmapped, ambiguous, and version-fallback cases are visible.
- **Human accountability:** clinical and sponsor-specific decisions have owners and status.
- **Reproducibility:** every output can be regenerated from pinned inputs and mappings.
- **Measurable value:** automation claims are supported by workflow and quality metrics.

## Current Boundary

The active roadmap remains the REDCap POC in `SPEC.md` and `VERSION_ROADMAP.md`. Authentication,
multi-tenancy, production infrastructure, protocol authoring, and additional EDC adapters remain
post-POC investments.
