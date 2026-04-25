# Business Value Analysis: USDM → EDC Transformation

*Research conducted: April 2026*

## The Problem in Plain Language

Every clinical trial has to go through roughly this sequence:

1. Scientists design the study (drug, dose, patient population, what will be measured, when)
2. Medical writers turn that design into a Protocol (100–200 page legal/regulatory document)
3. Data managers read the protocol and manually build the EDC system (the software clinical
   sites use to enter patient data)
4. Medical writers write CRF Completion Guidelines (telling site staff how to fill in every field)
5. The EDC is tested against the protocol — discrepancies found, fixes made, repeat
6. The trial starts. A Protocol Amendment happens. Return to step 2.

Steps 3, 4, and 5 happen today by a human reading a document and manually re-entering the same
information in a different system. This takes **6 to 16 weeks** for a moderately complex study.
It is error-prone. Protocol amendments — which happen in virtually every trial — restart a
significant portion of that cycle.

A USDM → EDC adapter collapses steps 3 and part of 4 from weeks to hours.

## Layer 1: Speed

EDC setup time from 8–16 weeks to days or hours. For a Phase III trial where site activation is
blocked until the EDC is ready, shaving 6 weeks off setup time has a direct dollar value. At
typical trial burn rates of $50K–$500K per day across sites, this is not abstract.

## Layer 2: Protocol-EDC Fidelity

One of the persistent problems in clinical data is the gap between what the protocol says and
what the EDC actually captures. A medical writer defines "systolic blood pressure" in the protocol.
Different EDC programmers on different studies create:

- `SBP_RESULT` with validation 0–300
- `SYSBP` with validation 60–200
- `BPSYS` with no units field

Now three studies measuring the same thing store it three different ways. Pooling data for a
regulatory submission or meta-analysis requires manual reconciliation. Regulators notice this.
They issue findings. People write responses. It takes months.

USDM BiomedicalConcepts are CDISC-coded. Blood pressure is `C49677`. When the adapter generates
the EDC from that concept, every study gets the same field name, the same validation range, the
same units. Consistency becomes structural, not dependent on individual programmer judgment.

## Layer 3: Amendment Propagation

Protocol amendments are essentially universal in late-phase trials. A sponsor adds a secondary
endpoint. A safety signal requires adding an assessment visit. A regulatory agency requests an
additional biomarker.

**Today:** Amendment → medical writing (new protocol version) → data management reads the delta
and decides what to change in the EDC → change made → re-tested. Weeks, minimum.

**With USDM as upstream source of truth:** The study definition changes in USDM → the adapter
re-runs → EDC delta generated automatically. "What changed?" is answered by diffing USDM versions
rather than a human reading two 150-page protocol PDFs side by side.

## Layer 4: Medical Writing Documents That Partially Write Themselves

CRF Completion Guidelines are largely a restatement of information that already exists in the EDC:
field name, label, valid values, units, instructions. This document is written by hand, reviewed
against the EDC by hand, and updated by hand every time the EDC changes.

If the EDC is generated from USDM, the Completion Guidelines can be generated from the same USDM
source. A human still writes instructional prose, but the structure, field names, valid ranges,
and coded values are auto-populated. This is roughly 40–60% of manual effort in CRF Completion
Guidelines, eliminated.

The same applies (partially) to:
- Data Management Plans (variable definition sections)
- Data Review Guidelines
- Statistical Analysis Plans (endpoint variable definitions)

## Layer 5: Downstream Regulatory Data Quality

FDA and EMA require submissions to include patient data in CDISC SDTM (raw) and ADaM
(analysis-ready) formats. Generating those datasets from EDC data that was built from USDM
BiomedicalConcepts is substantially easier, because the USDM→SDTM variable mapping is already
implicit in the BiomedicalConcept definition.

A significant proportion of Complete Response Letters (FDA rejection letters for drug applications)
include data standardization findings. Fixing SDTM/ADaM issues post-collection is enormously
expensive. Preventing them at the design stage via USDM-native EDC builds is a much cheaper
intervention.

## Beyond EDC: The Full Downstream Map

The same USDM study definition feeds other systems that also get built manually:

| System | Currently manual | USDM automation potential |
|---|---|---|
| EDC | Forms, visit schedule, edit checks | High — primary target |
| CTMS | Visit schedules, milestones | Medium — ScheduleTimeline maps directly |
| IxRS (randomization) | Treatment arms, strata | Medium — StudyArm maps directly |
| Safety database | AE form fields | Medium — BiomedicalConcept AE subset |
| Statistical analysis system | Dataset specifications | Low-Medium — requires SAP context |

Each is a potential downstream adapter. The EDC adapter is the first and most valuable.

## The CRO Angle

Contract Research Organizations set up studies for multiple sponsors. Each sponsor has slightly
different ways of specifying the same concepts. A CRO's data management team spends significant
time normalizing this before they can start building.

If sponsors submit USDM files, a CRO can auto-generate EDC builds that are consistent across
sponsors. A CRO that can promise "EDC ready in 2 weeks instead of 12" from a USDM input has a
real competitive differentiator. This is a billable service.

## Domain Expert Validation

Before writing any transformation logic, validate these claims with the medical writing domain
expert on this project. Key questions to answer empirically:

- Which parts of CRF design are genuinely mechanical vs. require human judgment?
- Where does the protocol-EDC gap create the most downstream pain (data cleaning, site queries,
  regulatory findings)?
- What would a pharma data manager or medical writer actually pay to solve — and which problems
  sound big but are not actually prioritized?
- Which EDC systems are most prevalent in the studies she has worked on? (This should inform
  which target adapter to build first beyond REDCap.)
- Does the USDM standard's abstractions map cleanly to how studies are actually designed in
  practice, or are there systematic gaps?
