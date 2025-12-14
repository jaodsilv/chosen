"""FastAPI application entry point."""

import logging
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator, Dict

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import get_settings
from app.core.exceptions import AppException

logger = logging.getLogger(__name__)

# Get settings
settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan manager for startup and shutdown events."""
    # Configure logging at startup
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    # Startup
    logger.info(
        f"Starting {settings.app_name} API v{settings.app_version} "
        f"in {settings.env} mode"
    )
    # Initialize agent system, load configurations, verify data directories
    # These will be implemented as the application grows
    yield
    # Shutdown
    logger.info(f"Shutting down {settings.app_name} API")
    # Cleanup resources


# Create FastAPI app
app = FastAPI(
    title="AI Message Writer Assistant API",
    description="Backend API for intelligent recruitment communication",
    version=settings.app_version,
    docs_url="/api/docs" if settings.env != "production" else None,
    redoc_url="/api/redoc" if settings.env != "production" else None,
    lifespan=lifespan,
)

# CORS middleware (for web UI)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "X-Request-ID"],
)


# Custom exception handler
@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    """Handle application exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.error_type,
            "message": exc.message,
            "details": exc.details,
        },
    )


# Health check endpoint
@app.get("/health")
async def health_check() -> Dict[str, Any]:
    """Health check endpoint for monitoring and load balancers."""
    return {
        "status": "healthy",
        "version": settings.app_version,
        "environment": settings.env,
    }


# Root endpoint
@app.get("/")
async def root() -> Dict[str, str]:
    """Root endpoint with API information."""
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "docs": "/api/docs",
    }


# API routers will be added here as they are implemented:
# app.include_router(conversations.router, prefix="/api/v1/conversations",
#                    tags=["conversations"])
# app.include_router(messages.router, prefix="/api/v1/messages",
#                    tags=["messages"])
# app.include_router(analysis.router, prefix="/api/v1/analysis",
#                    tags=["analysis"])
# app.include_router(settings.router, prefix="/api/v1/settings",
#                    tags=["settings"])
# app.include_router(websocket.router, prefix="/api/v1/ws",
#                    tags=["websocket"])
