"""Normalize Biomedical Concept identity and its study activity context."""

import re
from collections import defaultdict

from usdm_model.wrapper import Wrapper

from app.models.study import (
    BiomedicalConceptPropertySummary,
    BiomedicalConceptSummary,
    ScheduledInstanceContext,
    SourceActivityContext,
)

_PACKAGE_PATTERN = re.compile(r"/packages/([^/]+)/", re.IGNORECASE)
_NCI_CODE_PATTERN = re.compile(r"^C\d+$", re.IGNORECASE)


def _parse_reference(reference: str) -> tuple[str, str | None, str | None]:
    """Return reference type, specialization name, and package identifier."""
    lowered = reference.lower()
    package_match = _PACKAGE_PATTERN.search(reference)
    package = package_match.group(1) if package_match else None

    if "/datasetspecializations/" in lowered:
        return "dataset_specialization", reference.rstrip("/").split("/")[-1], package
    if "/biomedicalconcepts/" in lowered:
        return "biomedical_concept", None, package
    if _NCI_CODE_PATTERN.fullmatch(reference):
        return "nci_code", None, None
    if reference.startswith(("https://", "http://")):
        return "external_url", None, package
    return "unknown", None, package


def _build_activity_contexts(wrapper: Wrapper) -> dict[str, list[SourceActivityContext]]:
    """Index Biomedical Concept IDs to activities and scheduled instances."""
    contexts: dict[str, list[SourceActivityContext]] = defaultdict(list)

    for study_version in wrapper.study.versions:
        for design in study_version.studyDesigns:
            scheduled_by_activity: dict[str, list[ScheduledInstanceContext]] = defaultdict(list)

            for timeline in design.scheduleTimelines:
                for instance in timeline.instances:
                    activity_ids = getattr(instance, "activityIds", None)
                    if not activity_ids:
                        continue
                    scheduled = ScheduledInstanceContext(
                        timeline_id=str(timeline.id),
                        timeline_name=timeline.name,
                        instance_id=str(instance.id),
                        instance_name=instance.name,
                        instance_label=instance.label,
                    )
                    for activity_id in activity_ids:
                        scheduled_by_activity[str(activity_id)].append(scheduled)

            for activity in design.activities:
                activity_id = str(activity.id)
                context = SourceActivityContext(
                    study_version=study_version.versionIdentifier,
                    study_design_id=str(design.id),
                    study_design_name=design.name,
                    activity_id=activity_id,
                    activity_name=activity.name,
                    activity_label=activity.label,
                    scheduled_instances=scheduled_by_activity.get(activity_id, []),
                )
                for concept_id in activity.biomedicalConceptIds:
                    contexts[str(concept_id)].append(context)

    return contexts


def normalize_biomedical_concepts(wrapper: Wrapper) -> list[BiomedicalConceptSummary]:
    """Return concepts with identifiers kept separate and activity context preserved."""
    activity_contexts = _build_activity_contexts(wrapper)
    results: list[BiomedicalConceptSummary] = []

    for study_version in wrapper.study.versions:
        for concept in study_version.biomedicalConcepts:
            standard_code = concept.code.standardCode
            reference_type, specialization, package = _parse_reference(concept.reference)
            properties = [
                BiomedicalConceptPropertySummary(
                    name=prop.name,
                    label=prop.label,
                    datatype=prop.datatype,
                    is_required=prop.isRequired,
                    is_enabled=prop.isEnabled,
                    standard_code=prop.code.standardCode.code,
                    response_code_count=len(prop.responseCodes),
                )
                for prop in concept.properties
            ]
            results.append(
                BiomedicalConceptSummary(
                    concept_id=str(concept.id),
                    name=concept.name,
                    label=concept.label,
                    reference=concept.reference,
                    reference_type=reference_type,
                    specialization=specialization,
                    package=package,
                    standard_code=standard_code.code,
                    standard_code_system=standard_code.codeSystem,
                    standard_code_version=standard_code.codeSystemVersion,
                    property_count=len(properties),
                    properties=properties,
                    source_activities=activity_contexts.get(str(concept.id), []),
                )
            )

    return results
