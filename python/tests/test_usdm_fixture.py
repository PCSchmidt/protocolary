"""Gate 1 — Schema tests.

Validates three things:
  1. The sample fixture is valid USDM v4.x JSON (parses via usdm_model.Wrapper).
  2. The USDM object graph matches the hierarchy documented in MEMORY_SEMANTIC.md
     (with the correction from Gate 1 exploration: BiomedicalConcepts live on
     StudyVersion, not StudyDesign).
  3. The fixture can be stored in and retrieved from MongoDB with the schema
     defined in Decision 007 (app/models/study.py).

Run with:
    docker compose --profile test up -d mongo_test
    cd python && pytest tests/test_usdm_fixture.py -v
"""

from datetime import UTC, datetime

import pytest
from motor.motor_asyncio import AsyncIOMotorDatabase
from usdm_model.biomedical_concept import BiomedicalConcept
from usdm_model.study_design import InterventionalStudyDesign
from usdm_model.wrapper import Wrapper

# Expected BiomedicalConcept NCI codes for the vital signs POC set
EXPECTED_BC_CODES = {
    "C49677",  # Systolic Blood Pressure
    "C25299",  # Diastolic Blood Pressure
    "C49673",  # Heart Rate
    "C49678",  # Respiratory Rate
    "C25206",  # Body Temperature
    "C25347",  # Height
    "C29463",  # Weight
    "C16358",  # Body Mass Index
}


# ── Fixture parsing tests (no database) ───────────────────────────────────────


def test_fixture_parses_as_wrapper(sample_study_json: dict) -> None:
    """The sample JSON round-trips cleanly through Wrapper.model_validate."""
    wrapper = Wrapper.model_validate(sample_study_json)
    assert wrapper.usdmVersion == "4.0.0"
    assert wrapper.study is not None


def test_fixture_usdm_version(sample_study_json: dict) -> None:
    """The fixture targets USDM v4.x."""
    wrapper = Wrapper.model_validate(sample_study_json)
    major = int(wrapper.usdmVersion.split(".")[0])
    assert major == 4, f"Expected USDM v4.x, got {wrapper.usdmVersion}"


def test_study_has_one_version(sample_study_json: dict) -> None:
    """The study has exactly one StudyVersion (as expected for a simple POC fixture)."""
    wrapper = Wrapper.model_validate(sample_study_json)
    assert len(wrapper.study.versions) == 1


def test_biomedical_concepts_on_study_version(sample_study_json: dict) -> None:
    """BiomedicalConcepts live on StudyVersion, NOT on StudyDesign.

    This corrects the hierarchy shown in MEMORY_SEMANTIC.md (Gate 1 finding).
    """
    wrapper = Wrapper.model_validate(sample_study_json)
    sv = wrapper.study.versions[0]
    assert len(sv.biomedicalConcepts) == 8
    for bc in sv.biomedicalConcepts:
        assert isinstance(bc, BiomedicalConcept)


def test_vital_signs_nci_codes_present(sample_study_json: dict) -> None:
    """All 8 vital signs BiomedicalConcepts carry the correct CDISC NCI codes."""
    wrapper = Wrapper.model_validate(sample_study_json)
    sv = wrapper.study.versions[0]
    actual_codes = {bc.reference for bc in sv.biomedicalConcepts}
    assert actual_codes == EXPECTED_BC_CODES, (
        f"Missing codes: {EXPECTED_BC_CODES - actual_codes}; "
        f"Extra codes: {actual_codes - EXPECTED_BC_CODES}"
    )


def test_each_bc_has_at_least_one_property(sample_study_json: dict) -> None:
    """Every BiomedicalConcept has at least one BiomedicalConceptProperty."""
    wrapper = Wrapper.model_validate(sample_study_json)
    sv = wrapper.study.versions[0]
    for bc in sv.biomedicalConcepts:
        assert len(bc.properties) >= 1, f"{bc.name} has no properties"


def test_study_design_is_interventional(sample_study_json: dict) -> None:
    """The study design is an InterventionalStudyDesign with one arm and one epoch."""
    wrapper = Wrapper.model_validate(sample_study_json)
    sv = wrapper.study.versions[0]
    assert len(sv.studyDesigns) == 1
    design = sv.studyDesigns[0]
    assert isinstance(design, InterventionalStudyDesign)
    assert len(design.arms) == 1
    assert len(design.epochs) == 1


def test_wrapper_round_trips_to_json(sample_study_json: dict) -> None:
    """Wrapper.model_dump(mode='json') produces a dict that re-parses identically."""
    wrapper = Wrapper.model_validate(sample_study_json)
    dumped = wrapper.model_dump(mode="json")
    reparsed = Wrapper.model_validate(dumped)
    assert reparsed.study.name == wrapper.study.name
    assert len(reparsed.study.versions[0].biomedicalConcepts) == 8


# ── MongoDB schema tests (require test database) ──────────────────────────────


@pytest.mark.asyncio
async def test_study_stores_and_retrieves_from_mongodb(
    sample_study_json: dict,
    test_db: AsyncIOMotorDatabase,
) -> None:
    """A USDM Wrapper can be serialised and stored in MongoDB per Decision 007,
    then retrieved and re-parsed into a valid Wrapper."""
    wrapper = Wrapper.model_validate(sample_study_json)
    sv = wrapper.study.versions[0]

    # Build the document as defined in Decision 007.
    # NOTE: wrapper.study.id is a uuid.UUID object from the Pydantic model — always
    # wrap with str() before storing in MongoDB. model_dump(mode="json") handles this
    # automatically for the nested wrapper dict, but direct field access does not.
    doc = {
        "study_id": str(wrapper.study.id),
        "study_name": wrapper.study.name,
        "version_identifier": sv.versionIdentifier,
        "usdm_version": wrapper.usdmVersion,
        "created_at": datetime.now(UTC),
        "wrapper": wrapper.model_dump(mode="json"),  # nested dict, NOT a string
    }

    result = await test_db["studies"].insert_one(doc)
    assert result.inserted_id is not None

    # Retrieve and validate
    stored = await test_db["studies"].find_one({"study_id": str(wrapper.study.id)})
    assert stored is not None
    assert stored["study_name"] == "POC Vital Signs Adapter Study"
    assert stored["usdm_version"] == "4.0.0"

    # Confirm the nested wrapper dict re-parses as a valid Wrapper
    reparsed = Wrapper.model_validate(stored["wrapper"])
    assert len(reparsed.study.versions[0].biomedicalConcepts) == 8


@pytest.mark.asyncio
async def test_bc_query_from_stored_document(
    sample_study_json: dict,
    test_db: AsyncIOMotorDatabase,
) -> None:
    """BiomedicalConcepts can be extracted from a stored document without
    loading the entire Wrapper — querying the nested wrapper dict directly."""
    wrapper = Wrapper.model_validate(sample_study_json)
    sv = wrapper.study.versions[0]
    doc = {
        "study_id": str(wrapper.study.id),
        "study_name": wrapper.study.name,
        "version_identifier": sv.versionIdentifier,
        "usdm_version": wrapper.usdmVersion,
        "created_at": datetime.now(UTC),
        "wrapper": wrapper.model_dump(mode="json"),
    }
    await test_db["studies"].insert_one(doc)

    # Retrieve only the BC list via a projection
    stored = await test_db["studies"].find_one(
        {"study_id": str(wrapper.study.id)},
        {"wrapper.study.versions": 1},
    )
    assert stored is not None
    bcs = stored["wrapper"]["study"]["versions"][0]["biomedicalConcepts"]
    assert len(bcs) == 8
    references = {bc["reference"] for bc in bcs}
    assert "C49677" in references  # Systolic BP
