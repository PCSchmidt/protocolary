# DEMO_CHECKS.md — Protocolary | Demo Verification Checklist
# Run this checklist before DEMO APPROVED.
# Adapted from Blueprint's VISUAL_CHECKS.md for a backend API + Streamlit POC.

## Gate 4 Pre-Approval Checklist

Run through the entire checklist with a non-technical observer (ideally the domain expert).
All items must be CHECK before typing `DEMO APPROVED`.

### Streamlit Dashboard

**Upload Screen**
- [ ] Page loads without errors at `http://localhost:8501`
- [ ] "Upload USDM JSON" file picker accepts `.json` files
- [ ] Uploading a valid USDM file shows a success message with study title and version
- [ ] Uploading an invalid file shows a clear error message (not a Python traceback)
- [ ] Uploading a USDM file for a study already in the database handles gracefully

**Inspect Screen**
- [ ] Study title, version, and sponsor name display correctly
- [ ] Study arms table shows all arms with correct names
- [ ] BiomedicalConcepts table shows concept name, CDISC code, and property count
- [ ] Schedule timeline summary is readable (number of visits, assessment types)
- [ ] All vital signs concepts are visible in the concept list

**Map Screen**
- [ ] USDM concept → REDCap field mapping table renders for all vital signs
- [ ] Each row shows: USDM concept name | CDISC code | REDCap variable name | field type | valid range
- [ ] Unmapped concepts (if any) are flagged clearly — not silently dropped
- [ ] The mapping table is readable without clinical informatics knowledge

**Export Screen**
- [ ] "Download CSV" button produces a downloadable `.csv` file
- [ ] Downloaded CSV opens in Excel without errors
- [ ] CSV has the correct REDCap Data Dictionary column headers
- [ ] Field names are ≤ 26 characters (REDCap constraint)
- [ ] "Push to REDCap" button shows a confirmation step before pushing
- [ ] After push: success message shows number of instruments created in REDCap
- [ ] After push: REDCap sandbox project shows the correct instruments (verify manually)

### API Direct Verification

- [ ] `GET http://localhost:8000/health` returns `{"status": "ok", "mongo": "connected"}`
- [ ] `GET http://localhost:8000/docs` loads the OpenAPI documentation without errors
- [ ] All endpoints listed in API_REGISTRY.md appear in the OpenAPI docs

### End-to-End Timing

- [ ] A non-technical observer completes the full Upload → Inspect → Map → Export workflow
      in **under 5 minutes** without assistance

### Data Accuracy Spot Check (domain expert)

Ask the medical writing domain expert to verify:
- [ ] Systolic blood pressure maps to a "text/integer" field with range 60–250 mmHg
- [ ] All 8 vital signs concepts from SPEC.md appear in the REDCap instrument
- [ ] The REDCap form structure makes sense as a CRF (correct form names, field order)
- [ ] No clinically important information from the USDM definition is silently lost

## Post-Demo Notes

Record any observations here after the demo session:

```
[Empty — populated after Gate 4 demo session]
```
