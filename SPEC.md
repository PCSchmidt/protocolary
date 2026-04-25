# Project Specification

*Version: 0.1 — April 2026*
*Status: DRAFT — requires explicit approval before any code is written*

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

This spec must be explicitly confirmed before the Python project scaffold is created.
No code is written against unconfirmed scope.
