# Commercial Landscape: DDF/USDM Solutions

*Research conducted: April 2026*

## Market Context

- Approximately 25 organizations have publicly demonstrated DDF-compatible solutions as of early 2026
- USDM v4.0 released early 2025; stable, no major revision planned for 2026 beyond bug fixes
  and ICH M11 alignment
- TransCelerate member companies collectively invest $125B/year in R&D
- TransCelerate runs quarterly DDF Solution Showcases (September, December, March, July)
- The DDF Solution Directory at https://transcelerate.github.io/ddf-directory/directory/directory.html
  is self-reported and maintained by TransCelerate

## Tier 1: Enterprise Platforms (Dominant, Not USDM-Native)

These companies own the majority of the EDC market. DDF compatibility is on their roadmaps
but is not their core architecture. They are large ships that turn slowly.

### Medidata Rave EDC (Dassault Systèmes)
- Market leader by volume: 26% of global trial starts; 72% of 2024 FDA novel drug approvals
- 50+ pre-built connectors to other clinical systems
- DDF approach: integration-layer compatibility, not native USDM ingestion
- Proprietary DDF connector, bundled into enterprise contracts
- **Threat level to this project:** Low. They serve large pharma with enterprise contracts.

### Veeva Vault EDC
- Deep ecosystem integration across Vault platform (RIM, eTMF, CTMS, EDC all connected)
- April 2026 release added Clinical Ops–EDC and RIM connections
- No publicly announced native USDM ingestion; value prop is Veeva-to-Veeva integration
- **Threat level to this project:** Low. Same enterprise market as Medidata.

### Oracle Clinical One
- Added AI-enabled EHR interoperability in 2025
- Unified EDC with safety database (Argus)
- Proprietary integration rather than open USDM-first architecture
- **Threat level to this project:** Low. Enterprise-only.

**The Tier 1 pattern:** All three are adding connectivity features but none have made USDM the
core input format for EDC setup. They are checking a compliance box, not rebuilding around
the standard. Their DDF connectors require their own EDC system.

## Tier 2: Specialist Startups (Active DDF Field)

These companies have built products that are USDM-native or DDF-first. This is the active
competitive field.

### CRScube (cubeCDMS + cubeCTMS)
- Presented at July 2025 DDF Solution Showcase: "Embracing USDM standards to accelerate
  eClinical technology setup"
- Unified CTMS + EDC suite with USDM ingestion for EDC configuration automation
- **Closest direct competitor to this project's downstream adapter concept**
- Differentiator gap: CRScube requires their own EDC system. This project targets
  EDC-agnostic transformation (works with EDCs the sponsor already has).

### studyOS / Sitero (acquired November 2025)
- studyOS built "Ash," an AI clinical trial agent (natural language interface for trial workflows)
- Presented at July 2025 Showcase: "How USDM powers effective AI use in clinical trials"
- Acquired by Sitero (a CRO) in November 2025 — signal that CROs see AI-on-USDM as a
  competitive differentiator worth acquiring
- **Lesson:** The CRO acquisition market is active in this space.

### Indegene — Next Digital Protocol
- Protocol authoring solution outputting USDM v3.0 compliant JSON + human-readable PDF
- **Upstream-focused:** structured protocol creation → USDM. Not an EDC automation tool.
- Differentiator gap: addresses the input side, not the output side.

### Sycamore Informatics — SPA (Structured Protocol Authoring)
- Cloud-based collaborative protocol authoring with downstream hooks for CRF builds, CTMS, EDC
- **Upstream-focused** with integration hooks. Not a standalone EDC adapter.
- Clinical trial-aware framework with deep CDISC standards knowledge (USDM, SDTM, ADaM)

### Trialynx (EZ Research Solutions)
- AI-powered platform generating "fully aligned protocols, consents, study plans, IBs, and site
  documents" from a study plan
- In the DDF directory; positioned as end-to-end AI generation
- **Upstream-focused.** Not a transformation layer.

### NNIT
- Danish IT consultancy. September 2024 Showcase: "Enhancing Protocol Digitalization: FHIR and
  USDM in Action"
- Systems integrator building USDM connectors for clients, not a product company

### EQTY Life Sciences & ClinLine
- September 2024 Showcase: "Utilizing USDM to Unlock Real-World Data Potential"
- Different angle: USDM as bridge to real-world data, not EDC automation

### Espero Health / Nurocor
- Focus on ICH M11 + USDM regulatory alignment, not operational EDC automation

## Tier 3: Open Source (Most Significant Free Competitor)

### OpenStudyBuilder — Novo Nordisk
- Open-sourced internal study builder under MIT/GPLv3
- USDM-compatible with DDF API adaptor; supports ICH M11 and trial registration
- 2025 roadmap includes CRF library to enable EDC automation
- Institutional backing from one of the world's largest pharma companies
- Active community of commercial service providers building on top of it
- Costs nothing to use
- **Threat level to this project:** Medium. It is upstream-focused (study definition management)
  but moving toward EDC automation. However, it requires adopting Novo Nordisk's stack and is
  not EDC-agnostic. Monitor actively.

## The Critical Gap

```
Protocol Authoring  →  USDM JSON  →  EDC Configuration  →  Data Collection
   [CROWDED]           [standard]      [UNDERDEVELOPED]       [established]
```

Most commercial energy is on the **left side** — getting a protocol into USDM format
(Indegene, Sycamore, Trialynx, OpenStudyBuilder). The standard creation problem is being
actively solved.

The **right side — USDM JSON → working EDC configuration — is where the gap is.** CRScube
is the closest, but requires their own EDC system. There is no lightweight, EDC-agnostic,
open-standard downstream adapter that takes any USDM file and emits configurations for the
EDC system the sponsor already has.

That is the specific position this project can occupy.

## Competitive Position Summary

| Factor | Assessment |
|---|---|
| Market reality | Real. $125B/year R&D investment in member companies alone. |
| Upstream crowding | High. Protocol authoring → USDM is well-served. |
| Downstream crowding | Low. USDM → EDC configuration is underdeveloped. |
| Timing | Good. USDM v4.0 stable. Adoption accelerating. |
| Biggest free threat | OpenStudyBuilder (Novo Nordisk) — but upstream-focused, not EDC-agnostic |
| Closest commercial competitor | CRScube — but requires their own EDC |
| Defensible niche | EDC-agnostic downstream adapter; starts with REDCap, extends to Medidata/Veeva |

## Sources

- [DDF Solution Directory](https://transcelerate.github.io/ddf-directory/directory/directory.html)
- [TransCelerate DDF Initiative](https://www.transceleratebiopharmainc.com/initiatives/digital-data-flow/)
- [DDF Solution Showcase July 2025](https://www.transceleratebiopharmainc.com/events/webinar-digital-data-flow-ddf-solution-showcase-july-2025/)
- [DDF Solution Showcase September 2024](https://www.transceleratebiopharmainc.com/events/digital-data-flow-ddf-solution-showcase-fall-2024/)
- [CRScube USDM Article](https://www.crscube.io/resource/the-promise-and-challenges-of-the-unified-study-definition-model-(usdm))
- [OpenStudyBuilder](https://www.openstudybuilder.com/)
- [Sitero acquires studyOS](https://sitero.com/sitero-acquires-studyos/)
- [CDISC DDF](https://www.cdisc.org/ddf)
- [ICH M11 and DDF — Espero Health](https://espero-health.com/resources/modernizing_clinical_trials_ddf_ich-m11)
- [TransCelerate Digital Protocols Press Release](https://www.prnewswire.com/news-releases/transcelerate-advances-industrywide-shift-to-digital-protocols-302577913.html)
