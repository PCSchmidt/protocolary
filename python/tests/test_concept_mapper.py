"""Gate 3A.3 — governed EDC-neutral concept mapping tests."""

import json
from copy import deepcopy
from pathlib import Path

import pytest
from pydantic import ValidationError
from usdm_model.wrapper import Wrapper

from app.models.mapping import NeutralFieldDefinition, ValidationRule
from app.services.concept_identity import normalize_biomedical_concepts
from app.services.concept_mapper import ConceptMapper
from app.services.cosmos_provider import CosmosProvider

MAPPING_PATH = Path(__file__).parents[1] / "app" / "data" / "mappings" / "vital_signs.json"
COSMOS_DIR = Path(__file__).parents[1] / "app" / "data" / "cosmos"


@pytest.fixture(scope="module")
def mapper() -> ConceptMapper:
    """Return the mapper backed by checked-in governed data."""
    return ConceptMapper(CosmosProvider(COSMOS_DIR), MAPPING_PATH)


def test_mapping_library_contains_all_eight_vital_signs(mapper: ConceptMapper) -> None:
    """The POC mapping library covers exactly the scoped vital-sign set."""
    specializations = {mapping.source.specialization for mapping in mapper.library.mappings}

    assert specializations == {
        "SYSBP",
        "DIABP",
        "HR",
        "RESP",
        "TEMP",
        "HEIGHT",
        "WEIGHT",
        "BMI",
    }
    assert mapper.library.status == "draft"
    assert all(mapping.governance.status == "needs_review" for mapping in mapper.library.mappings)


def test_mapping_library_matches_pinned_cosmos_commit(mapper: ConceptMapper) -> None:
    """Mapping and standards versions cannot drift silently."""
    manifest = mapper.library_manifest()

    assert manifest["library_id"] == "poc-vital-signs"
    assert manifest["library_version"] == "0.1.0"
    assert manifest["cosmos_source_commit"] == mapper.cosmos_provider.source.commit


def test_mapping_identifiers_and_target_hints_are_unique(
    mapper: ConceptMapper,
) -> None:
    """Governed records and current target hints are collision-free."""
    mappings = mapper.library.mappings
    assert len({mapping.mapping_id for mapping in mappings}) == len(mappings)
    assert len({mapping.field.key for mapping in mappings}) == len(mappings)
    redcap_names = [mapping.field.target_hints["redcap"].variable_name for mapping in mappings]
    assert len(set(redcap_names)) == len(redcap_names)
    assert all(len(name) <= 26 for name in redcap_names)


def test_synthetic_legacy_concepts_map_by_name_without_code_collision(
    mapper: ConceptMapper, sample_study_json: dict
) -> None:
    """Names disambiguate stale synthetic codes that now identify other concepts."""
    concepts = normalize_biomedical_concepts(Wrapper.model_validate(sample_study_json))
    decisions = {decision.concept_name: decision for decision in mapper.map_concepts(concepts)}

    systolic = decisions["Systolic Blood Pressure"]
    heart_rate = decisions["Heart Rate"]
    assert systolic.mapping_id == "vitals-sysbp"
    assert systolic.match_basis == "name_alias"
    assert systolic.field is not None
    assert systolic.field.key == "systolic_blood_pressure"
    assert heart_rate.mapping_id == "vitals-heart-rate"
    assert heart_rate.field is not None
    assert heart_rate.field.key == "heart_rate"


def test_all_synthetic_vital_signs_map_but_require_review(
    mapper: ConceptMapper, sample_study_json: dict
) -> None:
    """The original eight-concept fixture maps without claiming clinical approval."""
    concepts = normalize_biomedical_concepts(Wrapper.model_validate(sample_study_json))
    decisions = mapper.map_concepts(concepts)

    assert len(decisions) == 8
    assert {decision.status for decision in decisions} == {"needs_review"}
    assert all(decision.field is not None for decision in decisions)
    assert all(decision.review_items for decision in decisions)


def test_real_dataset_specialization_maps_with_activity_context(
    mapper: ConceptMapper, cdisc_pilot_json: dict
) -> None:
    """A realistic repeated assessment maps by specialization and retains context."""
    concepts = normalize_biomedical_concepts(Wrapper.model_validate(cdisc_pilot_json))
    systolic = next(concept for concept in concepts if concept.name == "SBP2")
    decision = mapper.map_concept(systolic)

    assert decision.status == "needs_review"
    assert decision.match_basis == "specialization"
    assert decision.mapping_id == "vitals-sysbp"
    assert decision.field is not None
    assert decision.field.unit == "mmHg"
    assert decision.source_activities[0].activity_label == "Vital signs while supine"
    assert any("package differs" in item for item in decision.review_items)


def test_unscoped_real_concept_is_explicitly_unmapped(
    mapper: ConceptMapper, cdisc_pilot_json: dict
) -> None:
    """Concepts outside the POC scope are reported rather than discarded."""
    concepts = normalize_biomedical_concepts(Wrapper.model_validate(cdisc_pilot_json))
    race = next(concept for concept in concepts if concept.name == "Race")
    decision = mapper.map_concept(race)

    assert decision.status == "unmapped"
    assert decision.mapping_id is None
    assert decision.field is None
    assert decision.review_items


def test_neutral_field_contains_only_optional_target_hints(
    mapper: ConceptMapper,
) -> None:
    """Clinical field meaning exists independently from REDCap rendering hints."""
    mapping = next(
        item for item in mapper.library.mappings if item.source.specialization == "SYSBP"
    )
    field = mapping.field

    assert field.key == "systolic_blood_pressure"
    assert field.value_type == "integer"
    assert field.unit == "mmHg"
    assert field.validation == ValidationRule(minimum=60, maximum=250)
    assert field.target_hints["redcap"].variable_name == "systolic_bp"


def test_bmi_is_a_reviewable_derived_neutral_field(mapper: ConceptMapper) -> None:
    """BMI calculation is explicit but remains unapproved pending domain review."""
    mapping = next(item for item in mapper.library.mappings if item.source.specialization == "BMI")

    assert mapping.field.value_source == "derived"
    assert mapping.field.calculation is not None
    assert mapping.field.calculation.dependencies == ["weight", "height"]
    assert "calculated versus collected" in mapping.governance.review_items
    assert mapping.governance.status == "needs_review"


def test_invalid_numeric_bounds_are_rejected() -> None:
    """The neutral model rejects internally inconsistent field definitions."""
    with pytest.raises(ValidationError, match="minimum cannot exceed maximum"):
        ValidationRule(minimum=10, maximum=1)


def test_derived_field_without_calculation_is_rejected() -> None:
    """Derived fields cannot omit their dependency and expression definition."""
    with pytest.raises(ValidationError, match="derived fields require a calculation"):
        NeutralFieldDefinition(
            key="invalid",
            label="Invalid",
            value_type="decimal",
            unit=None,
            required=False,
            value_source="derived",
        )


def test_approved_mapping_returns_mapped_status(tmp_path: Path, sample_study_json: dict) -> None:
    """Technical behavior distinguishes approved mappings from review drafts."""
    library = json.loads(MAPPING_PATH.read_text(encoding="utf-8"))
    library["status"] = "approved"
    for mapping in library["mappings"]:
        mapping["governance"]["status"] = "approved"
        mapping["governance"]["review_items"] = []
    approved_path = tmp_path / "approved.json"
    approved_path.write_text(json.dumps(library), encoding="utf-8")
    approved_mapper = ConceptMapper(CosmosProvider(COSMOS_DIR), approved_path)
    concept = normalize_biomedical_concepts(Wrapper.model_validate(sample_study_json))[0]

    decision = approved_mapper.map_concept(concept)

    assert decision.status == "mapped"
    assert decision.governance is not None
    assert decision.governance.status == "approved"


def test_multiple_name_aliases_return_ambiguous(
    tmp_path: Path, mapper: ConceptMapper, sample_study_json: dict
) -> None:
    """Conflicting governed mappings produce an explicit ambiguous result."""
    library = json.loads(MAPPING_PATH.read_text(encoding="utf-8"))
    duplicate = deepcopy(library["mappings"][0])
    duplicate["mapping_id"] = "conflicting-sysbp"
    duplicate["source"]["specialization"] = "DIABP"
    duplicate["source"]["bc_id"] = "C25299"
    duplicate["field"]["key"] = "conflicting_systolic"
    duplicate["field"]["target_hints"]["redcap"]["variable_name"] = "conflicting_sysbp"
    library["mappings"].append(duplicate)
    ambiguous_path = tmp_path / "ambiguous.json"
    ambiguous_path.write_text(json.dumps(library), encoding="utf-8")
    ambiguous_mapper = ConceptMapper(CosmosProvider(COSMOS_DIR), ambiguous_path)
    concept = normalize_biomedical_concepts(Wrapper.model_validate(sample_study_json))[0]

    decision = ambiguous_mapper.map_concept(concept)

    assert decision.status == "ambiguous"
    assert decision.match_basis == "multiple"
    assert decision.field is None


def test_mapping_with_stale_cosmos_bc_id_is_rejected(tmp_path: Path) -> None:
    """A mapping library cannot load when source identifiers drift from COSMoS."""
    library = json.loads(MAPPING_PATH.read_text(encoding="utf-8"))
    library["mappings"][0]["source"]["bc_id"] = "C00000"
    invalid_path = tmp_path / "invalid-source.json"
    invalid_path.write_text(json.dumps(library), encoding="utf-8")

    with pytest.raises(ValueError, match="does not match COSMoS"):
        ConceptMapper(CosmosProvider(COSMOS_DIR), invalid_path)


def test_real_fixture_reports_both_scoped_and_unscoped_outcomes(
    mapper: ConceptMapper, cdisc_pilot_json: dict
) -> None:
    """A realistic study yields useful mappings without hiding out-of-scope concepts."""
    concepts = normalize_biomedical_concepts(Wrapper.model_validate(cdisc_pilot_json))
    decisions = mapper.map_concepts(concepts)
    statuses = {decision.status for decision in decisions}

    assert "needs_review" in statuses
    assert "unmapped" in statuses
    assert sum(decision.status == "needs_review" for decision in decisions) >= 10
