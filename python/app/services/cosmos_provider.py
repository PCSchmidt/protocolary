"""Offline lookups over a version-pinned subset of CDISC COSMoS exports."""

import csv
import json
import re
from collections import defaultdict
from pathlib import Path

from app.config import settings
from app.models.cosmos import (
    CosmosBiomedicalConceptProperty,
    CosmosDatasetVariable,
    CosmosLookupResult,
    CosmosMetadata,
    CosmosSource,
)
from app.models.study import BiomedicalConceptSummary

_PACKAGE_PATTERN = re.compile(r"/packages/([^/]+)/", re.IGNORECASE)
_DEFAULT_DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "cosmos"


class CosmosProvider:
    """Load immutable local CSV files and resolve USDM concept identities."""

    def __init__(self, data_dir: Path | None = None) -> None:
        configured_dir = Path(settings.cosmos_data_path)
        if data_dir is not None:
            self.data_dir = data_dir
        elif configured_dir.exists():
            self.data_dir = configured_dir
        else:
            self.data_dir = _DEFAULT_DATA_DIR
        manifest = json.loads((self.data_dir / "manifest.json").read_text(encoding="utf-8"))
        if manifest["source_commit"] != settings.cosmos_source_commit:
            raise ValueError("COSMoS snapshot commit does not match COSMOS_SOURCE_COMMIT")
        self.source = CosmosSource(
            repository=manifest["source_repository"],
            commit=manifest["source_commit"],
            commit_date=manifest["source_commit_date"],
            content_license=manifest["content_license"],
            attribution=manifest["attribution"],
        )
        self._concepts = self._load_biomedical_concepts()
        self._specializations = self._load_dataset_specializations()

    @staticmethod
    def _read_csv(path: Path) -> list[dict[str, str]]:
        with path.open(encoding="utf-8-sig", newline="") as csv_file:
            return list(csv.DictReader(csv_file))

    def _load_biomedical_concepts(self) -> dict[str, CosmosMetadata]:
        rows = self._read_csv(self.data_dir / "biomedical_concepts_vital_signs.csv")
        grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
        for row in rows:
            grouped[row["bc_id"].upper()].append(row)

        concepts: dict[str, CosmosMetadata] = {}
        for identifier, concept_rows in grouped.items():
            first = concept_rows[0]
            concepts[identifier] = CosmosMetadata(
                source_type="biomedical_concept",
                identifier=identifier,
                package_date=first["package_date"],
                short_name=first["short_name"],
                bc_id=first["bc_id"],
                ncit_code=first["ncit_code"],
                canonical_reference=(
                    f"/mdr/bc/packages/{first['package_date']}/" f"biomedicalconcepts/{identifier}"
                ),
                properties=[
                    CosmosBiomedicalConceptProperty(
                        dec_id=row["dec_id"],
                        ncit_dec_code=row["ncit_dec_code"],
                        label=row["dec_label"],
                        data_type=row["data_type"],
                        example_set=row["example_set"],
                        system=row["system"],
                        system_name=row["system_name"],
                        code=row["code"],
                    )
                    for row in concept_rows
                ],
            )
        return concepts

    def _load_dataset_specializations(self) -> dict[str, CosmosMetadata]:
        rows = self._read_csv(self.data_dir / "dataset_specializations_vital_signs.csv")
        grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
        for row in rows:
            grouped[row["vlm_group_id"].upper()].append(row)

        specializations: dict[str, CosmosMetadata] = {}
        for identifier, specialization_rows in grouped.items():
            first = specialization_rows[0]
            specializations[identifier] = CosmosMetadata(
                source_type="dataset_specialization",
                identifier=identifier,
                package_date=first["package_date"],
                short_name=first["short_name"],
                bc_id=first["bc_id"],
                ncit_code=first["bc_id"],
                canonical_reference=(
                    f"/mdr/specializations/sdtm/packages/{first['package_date']}/"
                    f"datasetspecializations/{identifier}"
                ),
                variables=[
                    CosmosDatasetVariable(
                        sdtm_variable=row["sdtm_variable"],
                        dec_id=row["dec_id"],
                        role=row["role"],
                        data_type=row["data_type"],
                        codelist=row["codelist"],
                        assigned_term=row["assigned_term"],
                        assigned_value=row["assigned_value"],
                        mandatory_variable=row["mandatory_variable"].upper() == "Y",
                        mandatory_value=row["mandatory_value"].upper() == "Y",
                    )
                    for row in specialization_rows
                ],
            )
        return specializations

    def _result(
        self,
        *,
        query: str,
        query_type: str,
        requested_package: str | None,
        matches: list[CosmosMetadata],
    ) -> CosmosLookupResult:
        if not matches:
            status = "not_found"
            version_match = "not_applicable"
        elif len(matches) > 1:
            status = "ambiguous"
            version_match = "not_applicable"
        else:
            status = "found"
            if requested_package is None:
                version_match = "not_applicable"
            elif matches[0].package_date == requested_package:
                version_match = "exact"
            else:
                version_match = "fallback"

        return CosmosLookupResult(
            status=status,
            query=query,
            query_type=query_type,
            requested_package=requested_package,
            version_match=version_match,
            matches=matches,
            source=self.source,
        )

    def lookup_specialization(
        self, identifier: str, requested_package: str | None = None
    ) -> CosmosLookupResult:
        """Resolve an SDTM Dataset Specialization identifier."""
        match = self._specializations.get(identifier.upper())
        return self._result(
            query=identifier,
            query_type="specialization",
            requested_package=requested_package,
            matches=[match] if match else [],
        )

    def lookup_nci_code(
        self,
        code: str,
        source_type: str | None = None,
        requested_package: str | None = None,
    ) -> CosmosLookupResult:
        """Resolve an NCI code, optionally constrained to one COSMoS record type."""
        normalized = code.upper()
        matches: list[CosmosMetadata] = []

        concept = self._concepts.get(normalized)
        if concept and source_type in (None, "biomedical_concept"):
            matches.append(concept)

        if source_type in (None, "dataset_specialization"):
            matches.extend(
                metadata
                for metadata in self._specializations.values()
                if metadata.bc_id.upper() == normalized
            )

        return self._result(
            query=code,
            query_type="nci_code",
            requested_package=requested_package,
            matches=matches,
        )

    def lookup_reference(self, reference: str) -> CosmosLookupResult:
        """Resolve a COSMoS URI or direct NCI-code reference."""
        package_match = _PACKAGE_PATTERN.search(reference)
        requested_package = package_match.group(1) if package_match else None
        identifier = reference.rstrip("/").split("/")[-1]
        lowered = reference.lower()

        if "/datasetspecializations/" in lowered:
            result = self.lookup_specialization(identifier, requested_package)
        elif "/biomedicalconcepts/" in lowered:
            result = self.lookup_nci_code(
                identifier,
                source_type="biomedical_concept",
                requested_package=requested_package,
            )
        else:
            result = self.lookup_nci_code(identifier)

        return result.model_copy(update={"query": reference, "query_type": "reference"})

    def resolve_concept(self, concept: BiomedicalConceptSummary) -> CosmosLookupResult:
        """Resolve a normalized USDM concept using its strongest identifier."""
        if concept.reference_type in {
            "dataset_specialization",
            "biomedical_concept",
            "nci_code",
        }:
            return self.lookup_reference(concept.reference)
        return self.lookup_nci_code(concept.standard_code)
