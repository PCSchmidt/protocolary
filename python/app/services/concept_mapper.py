"""Map normalized USDM concepts to governed EDC-neutral field definitions."""

import json
from collections import defaultdict
from pathlib import Path

from app.models.mapping import GovernedMapping, MappingDecision, MappingLibrary
from app.models.study import BiomedicalConceptSummary
from app.services.cosmos_provider import CosmosProvider

_DEFAULT_LIBRARY_PATH = (
    Path(__file__).resolve().parent.parent / "data" / "mappings" / "vital_signs.json"
)


def _normalize_name(value: str) -> str:
    return "".join(character for character in value.casefold() if character.isalnum())


class ConceptMapper:
    """Resolve concepts against a governed mapping library."""

    def __init__(
        self,
        cosmos_provider: CosmosProvider | None = None,
        library_path: Path | None = None,
    ) -> None:
        self.cosmos_provider = cosmos_provider or CosmosProvider()
        self.library_path = library_path or _DEFAULT_LIBRARY_PATH
        self.library = MappingLibrary.model_validate_json(
            self.library_path.read_text(encoding="utf-8")
        )
        if self.library.cosmos_source_commit != self.cosmos_provider.source.commit:
            raise ValueError("Mapping library and COSMoS snapshot commits do not match")
        self._validate_library_against_cosmos()
        self._by_specialization = {
            mapping.source.specialization.upper(): mapping for mapping in self.library.mappings
        }
        self._by_name: dict[str, list[GovernedMapping]] = defaultdict(list)
        self._by_current_code: dict[str, list[GovernedMapping]] = defaultdict(list)
        self._by_legacy_code: dict[str, list[GovernedMapping]] = defaultdict(list)
        for mapping in self.library.mappings:
            for alias in mapping.source.name_aliases:
                self._by_name[_normalize_name(alias)].append(mapping)
            self._by_current_code[mapping.source.bc_id.upper()].append(mapping)
            for code in mapping.source.legacy_codes:
                self._by_legacy_code[code.upper()].append(mapping)

    def _validate_library_against_cosmos(self) -> None:
        """Fail fast when governed source identifiers drift from pinned standards."""
        mapping_ids: set[str] = set()
        field_keys: set[str] = set()
        target_variables: set[tuple[str, str]] = set()

        for mapping in self.library.mappings:
            if mapping.mapping_id in mapping_ids:
                raise ValueError(f"Duplicate mapping_id: {mapping.mapping_id}")
            mapping_ids.add(mapping.mapping_id)

            if mapping.field.key in field_keys:
                raise ValueError(f"Duplicate neutral field key: {mapping.field.key}")
            field_keys.add(mapping.field.key)

            lookup = self.cosmos_provider.lookup_specialization(mapping.source.specialization)
            if lookup.status != "found" or len(lookup.matches) != 1:
                raise ValueError(
                    f"Mapping specialization did not resolve uniquely: "
                    f"{mapping.source.specialization}"
                )
            metadata = lookup.matches[0]
            if metadata.bc_id != mapping.source.bc_id:
                raise ValueError(
                    f"Mapping {mapping.mapping_id} bc_id {mapping.source.bc_id} "
                    f"does not match COSMoS {metadata.bc_id}"
                )

            for target, hint in mapping.field.target_hints.items():
                target_key = (target, hint.variable_name)
                if target_key in target_variables:
                    raise ValueError(f"Duplicate {target} variable name: {hint.variable_name}")
                target_variables.add(target_key)

    def _candidates(self, concept: BiomedicalConceptSummary) -> tuple[list[GovernedMapping], str]:
        if concept.specialization:
            mapping = self._by_specialization.get(concept.specialization.upper())
            if mapping:
                return [mapping], "specialization"

        name_matches = self._by_name.get(_normalize_name(concept.name), [])
        if len(name_matches) == 1:
            return name_matches, "name_alias"
        if len(name_matches) > 1:
            return name_matches, "multiple"

        current_matches = self._by_current_code.get(concept.standard_code.upper(), [])
        if len(current_matches) == 1:
            return current_matches, "current_bc_id"
        if len(current_matches) > 1:
            return current_matches, "multiple"

        legacy_matches = self._by_legacy_code.get(concept.standard_code.upper(), [])
        if len(legacy_matches) == 1:
            return legacy_matches, "legacy_code"
        if len(legacy_matches) > 1:
            return legacy_matches, "multiple"

        return [], "none"

    def map_concept(self, concept: BiomedicalConceptSummary) -> MappingDecision:
        """Map one concept without hiding ambiguity or review state."""
        cosmos_result = self.cosmos_provider.resolve_concept(concept)
        candidates, match_basis = self._candidates(concept)

        if not candidates:
            review_items = ["No governed vital-sign mapping matched this concept."]
            if cosmos_result.status == "ambiguous":
                review_items.append("COSMoS identity is ambiguous.")
            elif cosmos_result.status == "not_found":
                review_items.append("Concept was not found in the pinned COSMoS snapshot.")
            return MappingDecision(
                status="unmapped",
                concept_id=concept.concept_id,
                concept_name=concept.name,
                concept_reference=concept.reference,
                mapping_id=None,
                match_basis="none",
                field=None,
                governance=None,
                review_items=review_items,
                cosmos=cosmos_result,
                source_activities=concept.source_activities,
            )

        if len(candidates) > 1:
            return MappingDecision(
                status="ambiguous",
                concept_id=concept.concept_id,
                concept_name=concept.name,
                concept_reference=concept.reference,
                mapping_id=None,
                match_basis="multiple",
                field=None,
                governance=None,
                review_items=[
                    f"Multiple governed mappings matched: "
                    f"{', '.join(mapping.mapping_id for mapping in candidates)}"
                ],
                cosmos=cosmos_result,
                source_activities=concept.source_activities,
            )

        mapping = candidates[0]
        status = "mapped" if mapping.governance.status == "approved" else "needs_review"
        review_items = list(mapping.governance.review_items)
        if cosmos_result.version_match == "fallback":
            review_items.append("USDM reference package differs from the pinned COSMoS snapshot.")
        if cosmos_result.status == "not_found":
            review_items.append(
                "Mapping matched by compatibility metadata, but COSMoS did not resolve the concept."
            )
        elif cosmos_result.status == "ambiguous":
            review_items.append(
                "Mapping matched, but the concept's COSMoS identity remains ambiguous."
            )

        return MappingDecision(
            status=status,
            concept_id=concept.concept_id,
            concept_name=concept.name,
            concept_reference=concept.reference,
            mapping_id=mapping.mapping_id,
            match_basis=match_basis,
            field=mapping.field,
            governance=mapping.governance,
            review_items=review_items,
            cosmos=cosmos_result,
            source_activities=concept.source_activities,
        )

    def map_concepts(self, concepts: list[BiomedicalConceptSummary]) -> list[MappingDecision]:
        """Map concepts in stable input order."""
        return [self.map_concept(concept) for concept in concepts]

    def library_manifest(self) -> dict[str, str | int]:
        """Return compact version metadata for future transformation manifests."""
        raw = json.loads(self.library_path.read_text(encoding="utf-8"))
        return {
            "schema_version": raw["schema_version"],
            "library_id": raw["library_id"],
            "library_version": raw["library_version"],
            "status": raw["status"],
            "cosmos_source_commit": raw["cosmos_source_commit"],
        }
