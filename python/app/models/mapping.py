"""EDC-neutral field and governed mapping models."""

from typing import Literal

from pydantic import BaseModel, Field, model_validator

from app.models.cosmos import CosmosLookupResult
from app.models.study import SourceActivityContext


class ValidationRule(BaseModel):
    """Target-neutral numeric validation intent."""

    minimum: float | None = None
    maximum: float | None = None

    @model_validator(mode="after")
    def validate_bounds(self) -> "ValidationRule":
        if self.minimum is not None and self.maximum is not None and self.minimum > self.maximum:
            raise ValueError("minimum cannot exceed maximum")
        return self


class CalculationDefinition(BaseModel):
    """Target-neutral derived-field calculation."""

    expression: str
    dependencies: list[str]


class TargetHint(BaseModel):
    """Optional target-specific rendering hints, not the canonical field model."""

    variable_name: str
    form_name: str
    field_type: str
    validation_type: str


class NeutralFieldDefinition(BaseModel):
    """Clinical field meaning independent of any EDC implementation."""

    key: str
    label: str
    value_type: Literal["integer", "decimal", "text", "coded"]
    unit: str | None
    required: bool
    value_source: Literal["collected", "derived"]
    validation: ValidationRule | None = None
    calculation: CalculationDefinition | None = None
    target_hints: dict[str, TargetHint] = Field(default_factory=dict)

    @model_validator(mode="after")
    def validate_value_source(self) -> "NeutralFieldDefinition":
        if self.value_source == "derived" and self.calculation is None:
            raise ValueError("derived fields require a calculation")
        if self.value_source == "collected" and self.calculation is not None:
            raise ValueError("collected fields cannot define a calculation")
        return self


class MappingSource(BaseModel):
    """Standards identifiers and compatibility aliases for one governed mapping."""

    specialization: str
    bc_id: str
    legacy_codes: list[str]
    name_aliases: list[str]


class MappingGovernance(BaseModel):
    """Review state and rationale for a mapping decision."""

    status: Literal["draft", "needs_review", "approved", "retired"]
    rationale: str
    review_items: list[str]


class GovernedMapping(BaseModel):
    """One versioned mapping from standards identity to a neutral field."""

    mapping_id: str
    source: MappingSource
    field: NeutralFieldDefinition
    governance: MappingGovernance


class MappingLibrary(BaseModel):
    """Checked-in governed mapping library."""

    schema_version: int
    library_id: str
    library_version: str
    status: Literal["draft", "approved", "retired"]
    scope: str
    cosmos_source_commit: str
    mappings: list[GovernedMapping]


class MappingDecision(BaseModel):
    """Result of mapping one normalized USDM concept."""

    status: Literal["mapped", "needs_review", "unmapped", "ambiguous"]
    concept_id: str
    concept_name: str
    concept_reference: str
    mapping_id: str | None
    match_basis: Literal[
        "specialization",
        "name_alias",
        "current_bc_id",
        "legacy_code",
        "none",
        "multiple",
    ]
    field: NeutralFieldDefinition | None
    governance: MappingGovernance | None
    review_items: list[str]
    cosmos: CosmosLookupResult
    source_activities: list[SourceActivityContext]
