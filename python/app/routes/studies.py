"""Studies CRUD endpoints — Gate 2.

Five endpoints:
    POST   /studies                     Ingest a USDM study definition
    GET    /studies                     List all studies (metadata only)
    GET    /studies/{study_id}          Retrieve one study's full wrapper
    GET    /studies/{study_id}/arms     List study arms
    GET    /studies/{study_id}/concepts List BiomedicalConcepts with NCI codes

Path parameter {study_id} is the USDM wrapper.study.id (UUID string),
NOT the MongoDB ObjectId. Stored as str per Decision 007 / ERR-001.
"""

from datetime import UTC, datetime

from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from usdm_model.wrapper import Wrapper

from app.database import get_db
from app.models.study import BiomedicalConceptSummary, StudySummary
from app.services.concept_identity import normalize_biomedical_concepts

router = APIRouter()


# ── POST /studies ─────────────────────────────────────────────────────────────


@router.post("", status_code=status.HTTP_201_CREATED, summary="Ingest a USDM study")
async def create_study(
    body: dict,
    db: AsyncIOMotorDatabase = Depends(get_db),
) -> dict:
    """Validate and store a USDM v4.x JSON study definition.

    Request body must be a valid USDM Wrapper JSON object.
    Returns the stored study's identifiers on success.
    """
    try:
        wrapper = Wrapper.model_validate(body)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=f"Invalid USDM: {exc}",
        ) from exc

    sv = wrapper.study.versions[0]
    doc = {
        "study_id": str(wrapper.study.id),
        "study_name": wrapper.study.name,
        "version_identifier": sv.versionIdentifier,
        "usdm_version": wrapper.usdmVersion,
        "created_at": datetime.now(UTC),
        "wrapper": wrapper.model_dump(mode="json"),
    }
    result = await db["studies"].insert_one(doc)
    return {
        "study_id": doc["study_id"],
        "study_name": doc["study_name"],
        "version_identifier": doc["version_identifier"],
        "mongo_id": str(result.inserted_id),
    }


# ── GET /studies ──────────────────────────────────────────────────────────────


@router.get("", summary="List all studies")
async def list_studies(
    db: AsyncIOMotorDatabase = Depends(get_db),
) -> list[StudySummary]:
    """Return metadata for all stored studies (no wrapper payload)."""
    projection = {
        "_id": 0,
        "study_id": 1,
        "study_name": 1,
        "version_identifier": 1,
        "usdm_version": 1,
        "created_at": 1,
    }
    cursor = db["studies"].find({}, projection)
    docs = await cursor.to_list(length=200)
    return [StudySummary(**doc) for doc in docs]


# ── GET /studies/{study_id} ───────────────────────────────────────────────────


@router.get("/{study_id}", summary="Retrieve a study")
async def get_study(
    study_id: str,
    db: AsyncIOMotorDatabase = Depends(get_db),
) -> dict:
    """Return full metadata + wrapper dict for one study."""
    doc = await db["studies"].find_one({"study_id": study_id}, {"_id": 0})
    if not doc:
        raise HTTPException(status_code=404, detail="Study not found")
    return doc


# ── GET /studies/{study_id}/arms ──────────────────────────────────────────────


@router.get("/{study_id}/arms", summary="List study arms")
async def get_study_arms(
    study_id: str,
    db: AsyncIOMotorDatabase = Depends(get_db),
) -> list[dict]:
    """Return all StudyArm objects from the study's InterventionalStudyDesign."""
    doc = await db["studies"].find_one(
        {"study_id": study_id},
        {"wrapper.study.versions": 1, "_id": 0},
    )
    if not doc:
        raise HTTPException(status_code=404, detail="Study not found")

    arms: list[dict] = []
    for sv in doc["wrapper"]["study"]["versions"]:
        for design in sv.get("studyDesigns", []):
            arms.extend(design.get("arms", []))
    return arms


# ── GET /studies/{study_id}/concepts ─────────────────────────────────────────


@router.get("/{study_id}/concepts", summary="List BiomedicalConcepts")
async def get_study_concepts(
    study_id: str,
    db: AsyncIOMotorDatabase = Depends(get_db),
) -> list[BiomedicalConceptSummary]:
    """Return normalized Biomedical Concepts and their activity context.

    BiomedicalConcepts live on StudyVersion (not StudyDesign) — Gate 1 finding.
    The reference URI, standard code, Dataset Specialization, properties, and source
    activities remain separate so downstream mappings do not collapse distinct meanings.
    """
    doc = await db["studies"].find_one(
        {"study_id": study_id},
        {"wrapper": 1, "_id": 0},
    )
    if not doc:
        raise HTTPException(status_code=404, detail="Study not found")

    try:
        wrapper = Wrapper.model_validate(doc["wrapper"])
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=f"Stored USDM is incompatible with the current parser: {exc}",
        ) from exc

    return normalize_biomedical_concepts(wrapper)
