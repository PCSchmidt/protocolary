"""Async MongoDB connection via Motor.

Usage:
    from app.database import get_db

    async def my_route(db: AsyncIOMotorDatabase = Depends(get_db)):
        ...

The client is created once at startup and closed at shutdown via the FastAPI lifespan.
"""

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.config import settings

# Module-level client — initialised in lifespan, closed on shutdown
_client: AsyncIOMotorClient | None = None


def get_client() -> AsyncIOMotorClient:
    """Return the module-level Motor client. Raises if not yet initialised."""
    if _client is None:
        raise RuntimeError("MongoDB client has not been initialised. Check lifespan setup.")
    return _client


def get_db() -> AsyncIOMotorDatabase:
    """FastAPI dependency: yield the application database."""
    return get_client()[settings.mongo_db_name]


async def connect() -> None:
    """Open the Motor client. Called from FastAPI lifespan on startup."""
    global _client
    _client = AsyncIOMotorClient(settings.mongo_url)
    # Verify connectivity — raises ServerSelectionTimeoutError if MongoDB is unreachable
    await _client.admin.command("ping")


async def close() -> None:
    """Close the Motor client. Called from FastAPI lifespan on shutdown."""
    global _client
    if _client is not None:
        _client.close()
        _client = None


async def ensure_indexes() -> None:
    """Create required indexes if they don't already exist.

    Indexes are idempotent — safe to call on every startup.
    Required indexes per MEMORY_SEMANTIC.md / Decision 007:
        - studies.study_id  (ascending, for lookup by study ID)
        - studies.(study_id, version_identifier)  (compound, for versioned lookups)
    """
    db = get_db()
    studies = db["studies"]
    await studies.create_index("study_id")
    await studies.create_index([("study_id", 1), ("version_identifier", 1)])
