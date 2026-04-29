"""FastAPI application entry point.

Gate 1 scope: health endpoint only — confirms the app starts and MongoDB is reachable.
Study CRUD endpoints are added in Gate 2.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import close, connect, ensure_indexes


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa: ARG001
    """Connect to MongoDB on startup; close cleanly on shutdown."""
    await connect()
    await ensure_indexes()
    yield
    await close()


app = FastAPI(
    title="Transcelerate DDF Adapter",
    description=(
        "Proof of concept: USDM v4.x study definition → REDCap EDC configuration. "
        "See SPEC.md for scope boundaries."
    ),
    version="0.1.0",
    lifespan=lifespan,
)


@app.get(
    "/health",
    summary="Health check",
    description="Returns 200 when the API is running and MongoDB is reachable.",
    tags=["health"],
)
async def health() -> dict[str, str]:
    """Confirm service is alive and database connectivity is OK."""
    return {"status": "ok"}


# ── Gate 2: study endpoints added here ────────────────────────────────────────
# from app.routes import studies
# app.include_router(studies.router, prefix="/studies", tags=["studies"])
