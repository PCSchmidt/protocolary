# Vital-Signs Mapping Review

**Status:** Draft — domain review required  
**Mapping library:** `poc-vital-signs` v0.1.0  
**COSMoS source:** `fc11c9dbdc12aae709653b45c4c9db7f58824cf5`

This worksheet records the clinical decisions that COSMoS does not make for the product. Approval
requires a qualified reviewer to confirm or revise each row. Technical standards conformance is
not clinical approval.

| Concept | Unit | Type | Draft range | Required | Collection policy |
|---|---|---|---|---|---|
| Systolic Blood Pressure | mmHg | Integer | 60–250 | Yes | Collected |
| Diastolic Blood Pressure | mmHg | Integer | 40–150 | Yes | Collected |
| Heart Rate | beats/min | Integer | 30–250 | Yes | Collected |
| Respiratory Rate | breaths/min | Integer | 8–60 | Yes | Collected |
| Body Temperature | °C | Decimal | 35–42 | Yes | Collected |
| Height | cm | Decimal | 50–250 | Yes | Collected |
| Weight | kg | Decimal | 1–300 | Yes | Collected |
| BMI | kg/m² | Decimal | 10–80 | No | Draft: calculated |

## Review Questions

Use this framing question first:

> Imagine this vital-signs form will be used by a site during a real clinical trial. What would
> make it clinically sensible, unambiguous, and consistent with the protocol?

### Collection Requirements

1. Should systolic and diastolic blood pressure always be collected together?
2. Should heart rate be collected with every blood-pressure assessment?
3. Which measurements should be required, and when should "not done" be permitted?
4. Should the form capture why a required measurement was not performed?
5. Is height generally collected once, at baseline, or at every relevant visit?
6. Is weight collected at every visit or only at selected visits?

### Units

7. Should units be fixed or selectable?
8. Should temperature support Celsius, Fahrenheit, or both?
9. If multiple units are permitted, should values be converted automatically or stored exactly as
   entered?
10. Should units be fixed by sponsor standards, protocol, country/site, or another rule?

### Validation Ranges

11. Are these proposed ranges reasonable?

    - Systolic BP: 60–250 mmHg
    - Diastolic BP: 40–150 mmHg
    - Heart rate: 30–250 beats/min
    - Respiratory rate: 8–60 breaths/min
    - Temperature: 35–42°C
    - Height: 50–250 cm
    - Weight: 1–300 kg
    - BMI: 10–80 kg/m²

12. Should those ranges block entry, display a warning, or merely flag the value for review?
13. Do ranges vary by population—for example, pediatric, elderly, healthy-volunteer, or critically
    ill studies?
14. Are there values that should be technically accepted even though they require immediate
    verification?

### Measurement Context

15. Which measurement context must be captured?

    - Supine, sitting, or standing position
    - Rest period before measurement
    - Measurement or anatomical site
    - Device or method
    - Date and time
    - Before or after dosing

16. Must collection site or body position be separate fields for temperature and blood pressure?
17. Are there protocol instructions that should be displayed beside the fields?

### Repeated Assessments

18. If the protocol requires repeated measurements, should the form store every reading or only a
    calculated average?
19. How should repeat readings be labeled: Reading 1/2/3, timepoint, position, or another method?
20. Should each visit have its own vital-sign form, or should one repeatable form be used throughout
    the study?
21. For supine and standing blood pressure, should these be separate instruments, separate
    sections, or repeated rows on one form?
22. Should repeated assessments create separate fields, repeatable instruments, or longitudinal
    event instances?

### BMI

23. Should BMI be entered manually, calculated from height and weight, imported, or omitted?
24. If calculated, is `weight_kg / height_m²` the accepted formula?
25. How many decimal places should BMI use?
26. Should BMI recalculate whenever weight changes, or use height and weight collected at the same
    visit?
27. What should happen when height or weight is missing?

### Form Usability and Automation Boundaries

28. Are the labels and field ordering suitable for a recognizable vital-sign CRF?
29. What instructions should appear beside each field to prevent site confusion?
30. What information commonly appears in a real vital-sign CRF that the proposed fields are
    missing?
31. Which choices are usually determined by the protocol, sponsor standards, EDC conventions, or
    medical judgment?
32. Which mapping decisions can safely be automated across studies, and which always require human
    review?
33. Looking at the proposed form, would a coordinator know exactly what to collect without
    consulting another document?

If a question is outside the medical writer's role, mark it as requiring clinical data-management,
clinical, biostatistics, or EDC-build review rather than forcing an answer.

## Recommended Review Exercise

If possible, compare this worksheet field-by-field with a de-identified vital-sign CRF or protocol
schedule the reviewer knows well. Record:

- Missing fields
- Protocol-dependent decisions
- Sponsor-specific conventions
- Decisions unsuitable for automation
- Instructions required for site usability

## Approval Record

| Field | Value |
|---|---|
| Reviewer | Pending |
| Role/qualification | Pending |
| Review date | Pending |
| Mapping version reviewed | 0.1.0 |
| Outcome | Pending |
| Notes | Pending |
