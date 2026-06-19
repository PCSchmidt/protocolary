# Value Metrics

## Objective

Demonstrate economic and quality improvement using observed workflow data rather than generic
automation claims.

## Transformation Metrics

| Metric | Definition |
|---|---|
| Concepts discovered | Total USDM concepts considered by a transformation |
| Concepts resolved | Concepts linked to pinned standards metadata |
| Automated mapping rate | Mapped concepts ÷ concepts eligible for the scoped adapter |
| Review-required rate | Mappings requiring clinical or sponsor review ÷ eligible concepts |
| Unmapped rate | Concepts with no governed mapping ÷ eligible concepts |
| Fields generated | Neutral field definitions emitted |
| Target artifacts generated | Files or API payloads emitted successfully |
| Deterministic rerun | Whether identical versioned inputs produce the same output hash |

## Workflow Metrics

| Metric | Baseline | Automated |
|---|---:|---:|
| Time to interpret protocol assessments | TBD | Captured per transformation |
| Time to draft EDC specification | TBD | Captured per transformation |
| Human review time | TBD | Captured per review |
| Time to process an amendment | TBD | Captured per changed study version |
| Number of manual handoffs | TBD | Counted by workflow |

## Quality Metrics

- Import errors
- Duplicate or invalid field identifiers
- Missing required assessments
- Incorrect units or validation types
- Unresolved standards-version fallbacks
- Defects found during domain review
- Rework after target-system import

## Financial Model

For each workflow:

```text
estimated savings =
  baseline labor hours × loaded hourly cost
  - automated labor hours × loaded hourly cost
  - platform operating cost
```

Report assumptions separately from observed values. Do not present projected savings as realized
savings.

## Transformation-Run Record

Future transformation runs should capture:

- Study and version
- Source artifact hashes
- USDM, COSMoS, mapping-library, and adapter versions
- Counts for mapped, review-required, ambiguous, and unmapped concepts
- Generated-field and artifact counts
- Runtime
- Reviewer effort and approval status
- Output hashes

## POC Baseline Collection

During Gates 3A.3–3B, begin recording:

1. Time spent creating and reviewing each vital-sign mapping.
2. Number of decisions derived automatically from COSMoS.
3. Number requiring clinical judgment.
4. Time to generate and import the REDCap dictionary.
5. Defects found during live verification.
