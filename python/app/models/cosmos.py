"""Typed models for the pinned offline CDISC COSMoS snapshot."""

from typing import Literal

from pydantic import BaseModel, Field


class CosmosSource(BaseModel):
    """Immutable provenance for all records returned by the provider."""

    repository: str
    commit: str
    commit_date: str
    content_license: str
    attribution: str


class CosmosBiomedicalConceptProperty(BaseModel):
    """One property row from the COSMoS Biomedical Concept export."""

    dec_id: str
    ncit_dec_code: str
    label: str
    data_type: str
    example_set: str
    system: str
    system_name: str
    code: str


class CosmosDatasetVariable(BaseModel):
    """One variable row from an SDTM Dataset Specialization."""

    sdtm_variable: str
    dec_id: str
    role: str
    data_type: str
    codelist: str
    assigned_term: str
    assigned_value: str
    mandatory_variable: bool
    mandatory_value: bool


class CosmosMetadata(BaseModel):
    """Grouped BC or Dataset Specialization metadata."""

    source_type: Literal["biomedical_concept", "dataset_specialization"]
    identifier: str
    package_date: str
    short_name: str
    bc_id: str
    ncit_code: str
    canonical_reference: str
    properties: list[CosmosBiomedicalConceptProperty] = Field(default_factory=list)
    variables: list[CosmosDatasetVariable] = Field(default_factory=list)


class CosmosLookupResult(BaseModel):
    """Explicit lookup result; absence and ambiguity are never silent."""

    status: Literal["found", "not_found", "ambiguous"]
    query: str
    query_type: Literal["reference", "nci_code", "specialization"]
    requested_package: str | None
    version_match: Literal["exact", "fallback", "not_applicable"]
    matches: list[CosmosMetadata]
    source: CosmosSource
