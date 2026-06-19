"""Pytest configuration and shared fixtures.

All tests use a real MongoDB instance running on port 27018 (the test profile
in docker-compose.yml). No mocking of the database layer — see CLAUDE.md rules
and MEMORY_CORRECTIONS.md LESSON-004.

Start the test database before running the suite:
    docker compose --profile test up -d mongo_test
    pytest
"""

import json
from pathlib import Path

import pytest
import pytest_asyncio
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

FIXTURES_DIR = Path(__file__).parent / "fixtures"
PROTOCOL_EXPLORER_DIR = FIXTURES_DIR / "protocol_explorer"

# Test database coordinates — must match MONGO_TEST_URL / MONGO_TEST_DB_NAME
TEST_MONGO_URL = "mongodb://localhost:27018"
TEST_DB_NAME = "transcelerate_test"


@pytest.fixture(scope="session")
def sample_study_json() -> dict:
    """Return the USDM v4.x sample study fixture as a plain dict."""
    with open(FIXTURES_DIR / "sample_study.json") as f:
        return json.load(f)


@pytest.fixture(scope="session")
def cdisc_pilot_json() -> dict:
    """Return the pinned compatible CDISC Pilot fixture from Protocol Explorer."""
    with open(PROTOCOL_EXPLORER_DIR / "cdisc_pilot.json", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture(scope="session")
def observational_study_json() -> dict:
    """Return the pinned compatible observational fixture from Protocol Explorer."""
    with open(PROTOCOL_EXPLORER_DIR / "observational.json", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture(scope="session")
def incompatible_study_json() -> dict:
    """Return the pinned USDM 4.0 file expected to fail with usdm 0.67.0."""
    with open(
        PROTOCOL_EXPLORER_DIR / "incompatible_allergan_3111_302_001.json",
        encoding="utf-8",
    ) as f:
        return json.load(f)


@pytest_asyncio.fixture(scope="function")
async def test_db() -> AsyncIOMotorDatabase:
    """Async Motor database pointed at the isolated test MongoDB.

    Each test function gets a fresh database state: collections are dropped
    before the test runs and after it completes.
    """
    client: AsyncIOMotorClient = AsyncIOMotorClient(TEST_MONGO_URL)
    db: AsyncIOMotorDatabase = client[TEST_DB_NAME]

    # Clean slate before test
    await db["studies"].drop()

    yield db

    # Clean up after test
    await db["studies"].drop()
    client.close()
