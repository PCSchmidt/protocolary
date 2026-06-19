"""Gate 3A.1 — realistic fixture compatibility and concept identity tests."""

import hashlib
import json
from pathlib import Path

import pytest
from pydantic import ValidationError
from usdm_model.study_design import InterventionalStudyDesign
from usdm_model.wrapper import Wrapper

from app.services.concept_identity import normalize_biomedical_concepts

FIXTURE_DIR = Path(__file__).parent / "fixtures" / "protocol_explorer"


def test_protocol_explorer_manifest_hashes() -> None:
    """Every checked-in external fixture matches its recorded SHA-256 digest."""
    manifest = json.loads((FIXTURE_DIR / "manifest.json").read_text(encoding="utf-8"))

    for fixture in manifest["fixtures"]:
        fixture_path = FIXTURE_DIR / fixture["file"]
        digest = hashlib.sha256(fixture_path.read_bytes()).hexdigest()
        assert digest == fixture["sha256"], fixture["file"]


def test_cdisc_pilot_parses_with_pinned_usdm(cdisc_pilot_json: dict) -> None:
    """The primary realistic interventional fixture parses with usdm 0.67.0."""
    wrapper = Wrapper.model_validate(cdisc_pilot_json)
    study_version = wrapper.study.versions[0]

    assert wrapper.usdmVersion == "4.0"
    assert len(study_version.biomedicalConcepts) == 40
    assert len(study_version.studyDesigns[0].activities) == 40
    assert len(study_version.studyDesigns[0].scheduleTimelines) >= 1


def test_observational_fixture_records_source_classification_mismatch(
    observational_study_json: dict,
) -> None:
    """The observational-named source currently parses as interventional."""
    wrapper = Wrapper.model_validate(observational_study_json)
    design = wrapper.study.versions[0].studyDesigns[0]

    assert str(design.id) == "ObservationalStudyDesign_1"
    assert isinstance(design, InterventionalStudyDesign)
    assert len(wrapper.study.versions[0].biomedicalConcepts) == 7


def test_expected_incompatible_fixture_has_controlled_failure(
    incompatible_study_json: dict,
) -> None:
    """A declared USDM 4.0 file can still be incompatible with the pinned parser."""
    with pytest.raises(ValidationError, match="populationSummary"):
        Wrapper.model_validate(incompatible_study_json)


def test_dataset_specialization_identity_is_not_collapsed(
    cdisc_pilot_json: dict,
) -> None:
    """Dataset Specialization URI, package, and NCI code remain separate."""
    concepts = normalize_biomedical_concepts(Wrapper.model_validate(cdisc_pilot_json))
    systolic = next(concept for concept in concepts if concept.name == "SBP2")

    assert systolic.reference_type == "dataset_specialization"
    assert systolic.reference.endswith("/datasetspecializations/SYSBP")
    assert systolic.specialization == "SYSBP"
    assert systolic.package == "2025-04-01"
    assert systolic.standard_code == "C25298"


def test_concept_activity_and_schedule_context_is_preserved(
    cdisc_pilot_json: dict,
) -> None:
    """A repeated assessment remains linked to its activity and schedule instances."""
    concepts = normalize_biomedical_concepts(Wrapper.model_validate(cdisc_pilot_json))
    systolic = next(concept for concept in concepts if concept.name == "SBP2")

    assert len(systolic.source_activities) == 1
    activity = systolic.source_activities[0]
    assert activity.activity_label == "Vital signs while supine"
    assert activity.study_design_name
    assert activity.scheduled_instances
    assert any(
        instance.timeline_name == "Vital Sign Blood Pressure Timeline"
        for instance in activity.scheduled_instances
    )


def test_direct_nci_reference_remains_supported(sample_study_json: dict) -> None:
    """The small synthetic fixture still supports its direct NCI-code references."""
    concepts = normalize_biomedical_concepts(Wrapper.model_validate(sample_study_json))
    systolic = next(concept for concept in concepts if concept.name == "Systolic Blood Pressure")

    assert systolic.reference == "C49677"
    assert systolic.reference_type == "nci_code"
    assert systolic.specialization is None
    assert systolic.package is None
    assert systolic.source_activities == []
