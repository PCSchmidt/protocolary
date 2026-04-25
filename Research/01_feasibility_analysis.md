# Feasibility Analysis: TransCelerate DDF / StudyFlow Python Reboot

*Research conducted: April 2026*

## What the Original Repo Actually Was

The existing repo (PCSchmidt/transcelerate, `dev` branch) is essentially documentation and skeleton,
not working software. Concrete inventory:

- ~16KB of C# across a scaffolded Program.cs (936 bytes), Controllers/Models/Services folders,
  a .csproj, and a Dockerfile
- A 4.5KB `biomedical-concepts.json` seed file — the only real domain content produced
- Six forked TransCelerate repos as git submodules (none modified)
- Extensive strategy documents (the bulk of the actual work done)
- No auth, no tests, no end-to-end workflow, no running system

The POC was blocked on: authentication/authorization not implemented, no target EDC system selected,
no metrics collection, no end-to-end workflow tested.

The Python reboot is not a rewrite — it is a greenfield build with the strategy documents as input.
The `biomedical-concepts.json` is the one salvageable artifact.

## The Core Idea — Is It Real?

**Yes. The underlying problem is genuine and significant.**

Clinical trial study definitions are today manually re-entered into each downstream system:

```
Protocol Authoring → Study Builder → EDC System → CTMS → Data Management Platform
     (Word doc)        (vendor tool)   (Rave/Vault)  ...          ...
```

Each hand-off is error-prone, slow (weeks), and expensive. TransCelerate's DDF initiative
and the USDM (Unified Study Definitions Model) standard exist to replace those hand-offs with
machine-readable JSON that flows automatically. The Apache 2.0 license on all forked repos
explicitly permits commercial use.

The market is real — Veeva, Medidata/Dassault, Oracle, and a growing field of startups all have
DDF-related activity. A lighter-weight, EDC-agnostic Python adapter has a credible niche
(see `04_commercial_landscape.md`).

## Feasibility Verdict: Feasible — Scope It Sharply

The full "StudyFlow" vision (multi-tenant SaaS, pre-built adapters for every EDC, enterprise
analytics) is too broad for a solo part-time developer. The right POC is far narrower:
**one clean USDM → EDC transformation pipeline, end-to-end, with a real target system.**

### What Makes It Feasible Now (vs. a Year Ago)

| Factor | Status |
|---|---|
| USDM standard stability | USDM v4.0 released early 2025. Stable. No major revision planned for 2026. |
| Python USDM library | `usdm` PyPI package v0.67.0 (March 2026). Official CDISC/TransCelerate implementation. |
| Target EDC availability | REDCap: free sandbox, public REST API, no vendor NDA required |
| Developer language fit | Python vs. .NET — dramatically lower friction for this developer |

### What Makes It Hard

- USDM BiomedicalConcepts use CDISC-coded terminology. Mapping codes to EDC fields requires
  clinical domain knowledge. This is the hard, valuable part.
- The standard keeps evolving. Pin to a version; use the `usdm` package to track updates.
- Getting sandbox access to commercial EDCs (Medidata Rave, Veeva Vault) requires procurement.
  Start with REDCap to avoid blocking.
- TransCelerate DDF initiative pace has been slow (as of May 2024, still "setting up operations").
  Treat the existing open-source repos and USDM spec as stable inputs; do not depend on them
  shipping new tooling.

## Key Asset: Domain Expert

The developer's wife has 10+ years of medical writing experience in pharmaceutical clinical trials.
Before writing any transformation logic, sit down with her and walk through a real CRF she has
worked on. Map its fields to USDM BiomedicalConcepts manually. This exercise will reveal whether
the standard is rich enough to drive the EDC, or where the gaps are, faster than any amount of
reading the spec.
