"""Gate 2 — API tests.

Tests all five study endpoints plus the upgraded /health endpoint.
Uses httpx AsyncClient with FastAPI's ASGITransport so tests exercise the
full request/response cycle without a running server.

The lifespan's connect/close/ensure_indexes calls are patched to no-ops so
only the test MongoDB (port 27018) is required — the dev MongoDB at 27017
does not need to be running.

Run with:
    docker compose --profile test up -d mongo_test
    cd python && python -m pytest tests/test_studies_api.py -v
"""

from unittest.mock import AsyncMock

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.database import get_db
from app.main import app

# ── Test client fixture ───────────────────────────────────────────────────────


@pytest_asyncio.fixture
async def client(test_db: AsyncIOMotorDatabase, monkeypatch: pytest.MonkeyPatch):
    """Async HTTP client wired to the test database.

    Patches lifespan DB calls so only the test MongoDB (27018) is needed.
    """
    monkeypatch.setattr("app.database.connect", AsyncMock())
    monkeypatch.setattr("app.database.close", AsyncMock())
    monkeypatch.setattr("app.database.ensure_indexes", AsyncMock())

    app.dependency_overrides[get_db] = lambda: test_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()


# ── Helper ────────────────────────────────────────────────────────────────────


async def _ingest(client: AsyncClient, sample_study_json: dict) -> str:
    """POST the sample fixture and return the study_id."""
    r = await client.post("/studies", json=sample_study_json)
    assert r.status_code == 201, r.text
    return r.json()["study_id"]


# ── /health ───────────────────────────────────────────────────────────────────


async def test_health_ok(client: AsyncClient) -> None:
    """GET /health returns 200 with db: connected when MongoDB is reachable."""
    r = await client.get("/health")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "ok"
    assert data["db"] == "connected"


# ── POST /studies ─────────────────────────────────────────────────────────────


async def test_create_study_returns_201(client: AsyncClient, sample_study_json: dict) -> None:
    """POST /studies with a valid USDM fixture returns 201 and study identifiers."""
    r = await client.post("/studies", json=sample_study_json)
    assert r.status_code == 201
    data = r.json()
    assert "study_id" in data
    assert "study_name" in data
    assert "version_identifier" in data
    assert "mongo_id" in data
    assert data["study_name"] == "POC Vital Signs Adapter Study"


async def test_create_study_invalid_json_returns_422(client: AsyncClient) -> None:
    """POST /studies with a non-USDM dict returns 422."""
    r = await client.post("/studies", json={"not": "a usdm document"})
    assert r.status_code == 422
    assert "Invalid USDM" in r.json()["detail"]


# ── GET /studies ──────────────────────────────────────────────────────────────


async def test_list_studies_empty(client: AsyncClient) -> None:
    """GET /studies on empty DB returns an empty list."""
    r = await client.get("/studies")
    assert r.status_code == 200
    assert r.json() == []


async def test_list_studies_after_create(client: AsyncClient, sample_study_json: dict) -> None:
    """GET /studies after ingesting one study returns a list with one entry."""
    await _ingest(client, sample_study_json)
    r = await client.get("/studies")
    assert r.status_code == 200
    studies = r.json()
    assert len(studies) == 1
    assert studies[0]["study_name"] == "POC Vital Signs Adapter Study"
    # wrapper should NOT be in the list response
    assert "wrapper" not in studies[0]


# ── GET /studies/{study_id} ───────────────────────────────────────────────────


async def test_get_study_returns_full_wrapper(client: AsyncClient, sample_study_json: dict) -> None:
    """GET /studies/{id} returns the full stored study including wrapper."""
    study_id = await _ingest(client, sample_study_json)
    r = await client.get(f"/studies/{study_id}")
    assert r.status_code == 200
    data = r.json()
    assert data["study_id"] == study_id
    assert data["study_name"] == "POC Vital Signs Adapter Study"
    assert "wrapper" in data
    assert data["wrapper"]["usdmVersion"] == "4.0.0"


async def test_get_study_not_found(client: AsyncClient) -> None:
    """GET /studies/{id} for an unknown study_id returns 404."""
    r = await client.get("/studies/does-not-exist")
    assert r.status_code == 404
    assert r.json()["detail"] == "Study not found"


# ── GET /studies/{study_id}/arms ──────────────────────────────────────────────


async def test_get_arms_returns_one_arm(client: AsyncClient, sample_study_json: dict) -> None:
    """GET /studies/{id}/arms returns the single treatment arm from the fixture."""
    study_id = await _ingest(client, sample_study_json)
    r = await client.get(f"/studies/{study_id}/arms")
    assert r.status_code == 200
    arms = r.json()
    assert len(arms) == 1
    assert arms[0]["name"] == "Treatment Arm"


async def test_get_arms_not_found(client: AsyncClient) -> None:
    """GET /studies/{id}/arms for unknown study_id returns 404."""
    r = await client.get("/studies/does-not-exist/arms")
    assert r.status_code == 404


# ── GET /studies/{study_id}/concepts ─────────────────────────────────────────


async def test_get_concepts_returns_8_bcs(client: AsyncClient, sample_study_json: dict) -> None:
    """GET /studies/{id}/concepts returns all 8 vital signs BiomedicalConcepts."""
    study_id = await _ingest(client, sample_study_json)
    r = await client.get(f"/studies/{study_id}/concepts")
    assert r.status_code == 200
    concepts = r.json()
    assert len(concepts) == 8


async def test_get_concepts_nci_codes(client: AsyncClient, sample_study_json: dict) -> None:
    """GET /studies/{id}/concepts — all BCs have NCI reference codes."""
    study_id = await _ingest(client, sample_study_json)
    r = await client.get(f"/studies/{study_id}/concepts")
    assert r.status_code == 200
    concepts = r.json()
    references = {c["reference"] for c in concepts}
    assert "C49677" in references  # Systolic Blood Pressure
    assert "C25299" in references  # Diastolic Blood Pressure
    # Every BC must have a non-empty reference and standard_code
    for c in concepts:
        assert c["reference"], f"{c['name']} has empty reference"
        assert c["standard_code"], f"{c['name']} has empty standard_code"
        assert c["property_count"] >= 1, f"{c['name']} has no properties"
        assert c["reference_type"] == "nci_code"
        assert "properties" in c
        assert "source_activities" in c


async def test_get_concepts_normalizes_real_dataset_specializations(
    client: AsyncClient, cdisc_pilot_json: dict
) -> None:
    """The concepts endpoint preserves real COSMoS URI and activity identity."""
    study_id = await _ingest(client, cdisc_pilot_json)
    r = await client.get(f"/studies/{study_id}/concepts")

    assert r.status_code == 200
    concepts = r.json()
    systolic = next(concept for concept in concepts if concept["name"] == "SBP2")
    assert systolic["reference_type"] == "dataset_specialization"
    assert systolic["specialization"] == "SYSBP"
    assert systolic["package"] == "2025-04-01"
    assert systolic["standard_code"] == "C25298"
    assert systolic["source_activities"][0]["activity_label"] == "Vital signs while supine"


async def test_create_incompatible_real_study_returns_422(
    client: AsyncClient, incompatible_study_json: dict
) -> None:
    """A realistic but parser-incompatible USDM file fails clearly at ingestion."""
    r = await client.post("/studies", json=incompatible_study_json)

    assert r.status_code == 422
    assert "Invalid USDM" in r.json()["detail"]
    assert "populationSummary" in r.json()["detail"]


async def test_get_concepts_not_found(client: AsyncClient) -> None:
    """GET /studies/{id}/concepts for unknown study_id returns 404."""
    r = await client.get("/studies/does-not-exist/concepts")
    assert r.status_code == 404
