# Project Specification

*Version: 0.2 — June 18, 2026*
*Status: APPROVED — Gate 0 closed April 25, 2026*

## The One Question This POC Must Answer

> Can a USDM study definition be automatically transformed into a working EDC configuration?

## In Scope

| Item | Detail |
|---|---|
| USDM source format | USDM v4.x JSON (as produced by the `usdm` PyPI package) |
| Target EDC system | REDCap (Phase 1 adapter) |
| Study type | Single-arm study with vital signs assessments |
| BiomedicalConcept set | Vital signs subset: systolic BP, diastolic BP, heart rate, respiratory rate, temperature, height, weight, BMI |
| API | FastAPI REST service — store, retrieve, and transform USDM study definitions |
| Demo UI | Streamlit dashboard for stakeholder demonstration |
| Deployment | Local Docker Compose only |

## Approved External Data Sources

| Source | Role | Constraint |
|---|---|---|
| Protocol Explorer | Realistic USDM v4.x protocol fixtures, source PDFs, and conformance reports | Retain provenance and attribution; content may be partial and is not independently verified |
| TransCelerate `ddf-sdr-api` sample studies | Upstream source for many Protocol Explorer samples | Treat examples as evolving fixtures, not guaranteed complete protocol representations |
| CDISC `cdisc-org/COSMoS` | Biomedical Concepts and Dataset Specializations | Pin the selected export/package; tests must not depend on live network access |
| REDCap Data Dictionary export/template | Target metadata format | Obtain from the REDCap instance used for final verification |

Protocol Explorer and COSMoS are development inputs. They do not replace live REDCap verification
for Success Criterion 4.

## Explicitly Out of Scope for This POC

- Multi-tenancy or user authentication
- Production deployment or cloud infrastructure
- Adapters for any EDC system other than REDCap
- Protocol authoring or USDM generation (upstream)
- Full BiomedicalConcept library (laboratory, safety, PRO categories)
- Edit check / validation logic generation
- CRF Completion Guidelines document generation
- Commercial licensing, billing, or SaaS infrastructure
- Adapters for CTMS, IxRS, or safety database systems

## Success Criteria

1. A real USDM v4.x JSON file can be submitted to the API and stored
2. The stored study definition's BiomedicalConcepts (vital signs subset) are correctly parsed
3. The API generates a valid REDCap Data Dictionary CSV from the stored study definition
4. That CSV can be imported into a live REDCap project sandbox and produces correct instruments
5. A non-technical pharma stakeholder can complete the full workflow via the Streamlit UI
   in under 5 minutes without assistance

## Approval Gate

This spec was explicitly confirmed before the Python project scaffold was created. Scope changes
still require explicit approval; adding realistic fixtures and authoritative metadata sources does
not change the POC's target, study type, or Biomedical Concept subset.
