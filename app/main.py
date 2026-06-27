from __future__ import annotations

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.health import router as health_router
from app.api.router import api_router
from app.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    import os

    if not os.path.exists(settings.DATABASE_URL):
        import sys

        print(f"ERROR: Database not found at '{settings.DATABASE_URL}'", file=sys.stderr)
        print("Run: python scripts/init_db.py", file=sys.stderr)
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.API_TITLE,
        version=settings.API_VERSION,
        description=(
            "REST API for VAG (Volkswagen/Audi Group) Diagnostic Trouble Codes. "
            "Provides lookup, search, and cross-reference capabilities for DTC codes, "
            "component identifiers, and fault variants."
        ),
        lifespan=lifespan,
        docs_url="/",
        redoc_url="/redoc",
    )

    origins = [o.strip() for o in settings.ALLOWED_ORIGINS.split(",")]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["GET"],
        allow_headers=["*"],
    )

    app.include_router(health_router)
    app.include_router(api_router)

    return app


app = create_app()
