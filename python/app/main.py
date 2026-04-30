"""FastAPI application entry point."""

from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.database import close, connect, ensure_indexes, get_db
from app.routes import studies


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
    version="0.2.0",
    lifespan=lifespan,
)

app.include_router(studies.router, prefix="/studies", tags=["studies"])


@app.get(
    "/health",
    summary="Health check",
    description="Returns 200 when the API is running and MongoDB is reachable.",
    tags=["health"],
)
async def health(db: AsyncIOMotorDatabase = Depends(get_db)) -> dict[str, str]:
    """Confirm service is alive and database connectivity is OK."""
    try:
        await db.command("ping")
        return {"status": "ok", "db": "connected"}
    except Exception:
        return JSONResponse(
            status_code=503,
            content={"status": "error", "db": "unreachable"},
        )
