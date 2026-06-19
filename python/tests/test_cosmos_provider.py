"""Gate 3A.2 — pinned offline COSMoS metadata provider tests."""

import hashlib
import json
from pathlib import Path

import pytest
from usdm_model.wrapper import Wrapper

from app.services.concept_identity import normalize_biomedical_concepts
from app.services.cosmos_provider import CosmosProvider

COSMOS_DIR = Path(__file__).parents[1] / "app" / "data" / "cosmos"
VITAL_SPECIALIZATIONS = {
    "SYSBP": "C25298",
    "DIABP": "C25299",
    "HR": "C49677",
    "RESP": "C49678",
    "TEMP": "C174446",
    "HEIGHT": "C164634",
    "WEIGHT": "C81328",
    "BMI": "C16358",
}


@pytest.fixture(scope="module")
def cosmos_provider() -> CosmosProvider:
    """Return the provider backed only by checked-in local data."""
    return CosmosProvider(COSMOS_DIR)


def test_cosmos_snapshot_hashes_and_row_counts() -> None:
    """Derived files match the immutable provenance manifest."""
    manifest = json.loads((COSMOS_DIR / "manifest.json").read_text(encoding="utf-8"))

    for derived in manifest["derived_files"]:
        path = COSMOS_DIR / derived["file"]
        assert hashlib.sha256(path.read_bytes()).hexdigest() == derived["sha256"]
        with path.open(encoding="utf-8-sig") as data_file:
            assert sum(1 for _ in data_file) - 1 == derived["row_count"]


def test_provider_exposes_immutable_source(cosmos_provider: CosmosProvider) -> None:
    """Every lookup reports the pinned commit and content license."""
    result = cosmos_provider.lookup_specialization("SYSBP")

    assert result.source.commit == "fc11c9dbdc12aae709653b45c4c9db7f58824cf5"
    assert result.source.content_license == "CC BY 4.0"
    assert "COSMoS" in result.source.attribution


@pytest.mark.parametrize(("specialization", "bc_id"), VITAL_SPECIALIZATIONS.items())
def test_all_scoped_dataset_specializations_resolve(
    cosmos_provider: CosmosProvider,
    specialization: str,
    bc_id: str,
) -> None:
    """All eight scoped vital-sign specializations resolve offline."""
    result = cosmos_provider.lookup_specialization(specialization)

    assert result.status == "found"
    assert result.version_match == "not_applicable"
    assert len(result.matches) == 1
    metadata = result.matches[0]
    assert metadata.identifier == specialization
    assert metadata.bc_id == bc_id
    assert metadata.variables
    assert any(variable.mandatory_variable for variable in metadata.variables)


def test_reference_uri_resolves_with_explicit_version_fallback(
    cosmos_provider: CosmosProvider,
) -> None:
    """An older fixture URI resolves but reports the package-version mismatch."""
    reference = "/mdr/specializations/sdtm/packages/2025-04-01/" "datasetspecializations/SYSBP"
    result = cosmos_provider.lookup_reference(reference)

    assert result.status == "found"
    assert result.requested_package == "2025-04-01"
    assert result.version_match == "fallback"
    assert result.matches[0].package_date == "2026-05-26"


def test_exact_package_match_is_reported(cosmos_provider: CosmosProvider) -> None:
    """A caller can distinguish an exact package match from fallback metadata."""
    result = cosmos_provider.lookup_specialization("SYSBP", "2026-05-26")

    assert result.status == "found"
    assert result.version_match == "exact"


def test_nci_code_without_source_type_is_explicitly_ambiguous(
    cosmos_provider: CosmosProvider,
) -> None:
    """A code shared by a BC and specialization never resolves silently."""
    result = cosmos_provider.lookup_nci_code("C25298")

    assert result.status == "ambiguous"
    assert {match.source_type for match in result.matches} == {
        "biomedical_concept",
        "dataset_specialization",
    }


def test_nci_code_can_be_constrained_to_biomedical_concept(
    cosmos_provider: CosmosProvider,
) -> None:
    """Source-type constraints turn an ambiguous code into one result."""
    result = cosmos_provider.lookup_nci_code("C25298", source_type="biomedical_concept")

    assert result.status == "found"
    assert result.matches[0].short_name == "Systolic Blood Pressure"
    assert result.matches[0].properties


@pytest.mark.parametrize("legacy_code", ["C29463", "C25206", "C49673"])
def test_stale_legacy_codes_are_not_fabricated(
    cosmos_provider: CosmosProvider, legacy_code: str
) -> None:
    """Codes absent from the pinned source return not_found rather than aliases."""
    result = cosmos_provider.lookup_nci_code(legacy_code)

    assert result.status == "not_found"
    assert result.matches == []


def test_real_usdm_concept_resolves_by_dataset_specialization(
    cosmos_provider: CosmosProvider,
    cdisc_pilot_json: dict,
) -> None:
    """The provider consumes the normalized identity produced in Gate 3A.1."""
    concepts = normalize_biomedical_concepts(Wrapper.model_validate(cdisc_pilot_json))
    systolic = next(concept for concept in concepts if concept.name == "SBP2")
    result = cosmos_provider.resolve_concept(systolic)

    assert result.status == "found"
    assert result.matches[0].identifier == "SYSBP"
    assert result.version_match == "fallback"


def test_unknown_specialization_is_explicit_not_found(
    cosmos_provider: CosmosProvider,
) -> None:
    """Unknown identifiers produce a typed not-found result."""
    result = cosmos_provider.lookup_specialization("DOES_NOT_EXIST")

    assert result.status == "not_found"
    assert result.matches == []
