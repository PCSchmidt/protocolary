"""Pydantic response models for the studies collection.

These are NOT the usdm_model classes — those are used for parsing and validation.
These models define what the API returns and what is stored in MongoDB.

MongoDB schema (Decision 007):
    Collection:  studies
    Document:
        _id                : ObjectId  (MongoDB auto-generated; serialised as str in responses)
        study_id           : str       (wrapper.study.id — indexed)
        study_name         : str       (wrapper.study.name)
        version_identifier : str       (StudyVersion.versionIdentifier — indexed compound)
        usdm_version       : str       (wrapper.usdmVersion)
        created_at         : datetime
        wrapper            : dict      (full Wrapper.model_dump(mode='json') — nested, NOT a
                                        string blob; MongoDB can query into sub-fields)

    Indexes:
        study_id                           (ascending)
        (study_id, version_identifier)     (compound ascending)

Design rationale:
    - Store the full object graph as a nested dict so MongoDB can address sub-fields
      without deserialising the entire document.
    - Extract metadata fields at the top level to support efficient index-based queries
      (e.g. "give me study X version 2") without scanning the nested wrapper dict.
    - No attempt to flatten the USDM hierarchy into a relational-style schema — the graph
      is too deep and that would require significant ORM mapping work for no POC benefit.
"""

from datetime import datetime

from pydantic import BaseModel, Field


class StudySummary(BaseModel):
    """Lightweight response for list endpoints — id, name, version only."""

    study_id: str
    study_name: str
    version_identifier: str
    usdm_version: str
    created_at: datetime


class StudyInDB(StudySummary):
    """Full stored document shape (used internally; not directly returned by API)."""

    id: str = Field(alias="_id")  # MongoDB ObjectId serialised as str
    wrapper: dict  # full Wrapper.model_dump(mode='json')

    model_config = {"populate_by_name": True}


class BiomedicalConceptPropertySummary(BaseModel):
    """Normalized property metadata needed by downstream EDC mappings."""

    name: str
    label: str | None
    datatype: str
    is_required: bool
    is_enabled: bool
    standard_code: str
    response_code_count: int


class ScheduledInstanceContext(BaseModel):
    """One schedule instance in which an activity is performed."""

    timeline_id: str
    timeline_name: str
    instance_id: str
    instance_name: str
    instance_label: str | None


class SourceActivityContext(BaseModel):
    """Activity that links a Biomedical Concept into a study design."""

    study_version: str
    study_design_id: str
    study_design_name: str
    activity_id: str
    activity_name: str
    activity_label: str | None
    scheduled_instances: list[ScheduledInstanceContext]


class BiomedicalConceptSummary(BaseModel):
    """Single BiomedicalConcept as returned by GET /studies/{id}/concepts."""

    concept_id: str
    name: str
    label: str | None
    reference: str
    reference_type: str
    specialization: str | None
    package: str | None
    standard_code: str
    standard_code_system: str
    standard_code_version: str
    property_count: int
    properties: list[BiomedicalConceptPropertySummary]
    source_activities: list[SourceActivityContext]
