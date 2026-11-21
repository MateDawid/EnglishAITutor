import logging.config
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from logging_config import LOGGING_CONFIG
from utils.database import engine
from core.router import router as core_router
from auth.router import router as auth_router
from auth.constants import CSRF_TOKEN_HEADER_NAME
from auth.middleware import TrustedOriginCSRFMiddleware
from flashcards.router import router as flashcards_router
from conversations.router import router as conversations_router
from config import settings

logging.config.dictConfig(LOGGING_CONFIG)


@asynccontextmanager
async def lifespan(_app: FastAPI):
    yield
    await engine.dispose()


app = FastAPI(
    title="English AI Tutor API",
    description="An API to help learn English vocabulary by flashcards and chat with AI.",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.trusted_frontend_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "X-CSRF-Token"],
)
app.add_middleware(TrustedOriginCSRFMiddleware)

app.include_router(core_router, prefix="", tags=["core"])
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(flashcards_router, prefix="/flashcards", tags=["flashcards"])
app.include_router(conversations_router, prefix="/conversations", tags=["conversations"])


def custom_openapi() -> dict[str, Any]:
    """
    Add CSRF header authorization to unsafe operations in Swagger UI.

    Returns:
        dict[str, Any]: The generated OpenAPI schema.
    """
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    components = openapi_schema.setdefault("components", {})
    security_schemes = components.setdefault("securitySchemes", {})
    security_schemes["CSRFToken"] = {
        "type": "apiKey",
        "in": "header",
        "name": CSRF_TOKEN_HEADER_NAME,
        "description": "Get a token from GET /auth/csrf, then authorize with that token.",
    }

    unsafe_methods = {"post", "put", "patch", "delete"}
    for path_item in openapi_schema["paths"].values():
        for method, operation in path_item.items():
            if method in unsafe_methods:
                operation["security"] = [{"CSRFToken": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",  # noqa: S104
        port=8000,
        reload=True,
    )
