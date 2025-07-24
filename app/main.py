"""Main FastAPI application."""
import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from slowapi.middleware import SlowAPIMiddleware

from app.api import admin, auth, categories, tags, todos
from app.config import settings
from app.database import engine
from app.middleware.auth import AuthMiddleware
from app.middleware.error_handler import ErrorHandlerMiddleware
from app.middleware.logging import LoggingMiddleware
from app.middleware.rate_limit import limiter, setup_rate_limiting
from app.middleware.security import SecurityHeadersMiddleware
from app.middleware.monitoring import MonitoringMiddleware
from app.monitoring.telemetry import setup_telemetry, instrument_app
from app.redis import close_redis_pools
from prometheus_client import make_asgi_app

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Handle application lifecycle events."""
    logger.info("Starting up Todo API...")
    
    # Setup OpenTelemetry
    setup_telemetry(
        service_name="todo-api",
        service_version="1.0.0",
        otlp_endpoint=settings.otlp_endpoint if hasattr(settings, 'otlp_endpoint') else None
    )
    
    # Instrument the application
    instrument_app(app, engine.sync_engine)
    
    yield
    
    logger.info("Shutting down Todo API...")
    await engine.dispose()
    await close_redis_pools()


# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="A simple and robust Todo List Web API",
    openapi_url=f"{settings.api_v1_str}/openapi.json",
    docs_url=f"{settings.api_v1_str}/docs",
    redoc_url=f"{settings.api_v1_str}/redoc",
    lifespan=lifespan,
)

# Rate Limiting Setup
# Setup rate limiting
setup_rate_limiting(app)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.backend_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add custom middleware (order matters - error handler should be first)
app.add_middleware(ErrorHandlerMiddleware)
app.add_middleware(MonitoringMiddleware)  # Add monitoring middleware
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(AuthMiddleware)
app.add_middleware(LoggingMiddleware)

# Add SlowAPI middleware (must be after other middleware)
app.add_middleware(SlowAPIMiddleware)


# Request size limit middleware
@app.middleware("http")
async def limit_request_size(request: Request, call_next):
    """Limit request size to prevent DoS attacks."""
    from fastapi.responses import JSONResponse
    
    max_size = 10 * 1024 * 1024  # 10MB default
    if request.headers.get("content-length"):
        if int(request.headers["content-length"]) > max_size:
            return JSONResponse(
                status_code=413,
                content={"detail": "Request too large"}
            )
    return await call_next(request)

# Include routers
app.include_router(auth.router, prefix=f"{settings.api_v1_str}/auth", tags=["auth"])
app.include_router(
    categories.router,
    prefix=f"{settings.api_v1_str}/categories",
    tags=["categories"]
)
app.include_router(todos.router, prefix=f"{settings.api_v1_str}/todos", tags=["todos"])
app.include_router(tags.router, prefix=f"{settings.api_v1_str}/tags", tags=["tags"])
app.include_router(admin.router, prefix=f"{settings.api_v1_str}/admin", tags=["admin"])


@app.get("/")
@limiter.exempt
async def root() -> dict[str, str]:
    """Root endpoint."""
    return {
        "message": "Welcome to Todo API",
        "docs": f"{settings.api_v1_str}/docs",
        "health": "/health",
    }


@app.get("/health")
@limiter.exempt
async def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy", "app": settings.app_name}


@app.get("/api/v1/test-rate-limit")
@limiter.limit("5/minute")
async def test_rate_limit(request: Request) -> dict[str, str]:
    """Test endpoint for Rate Limiting with 5/minute."""
    return {"message": "Request successful", "limit": "5/minute"}


# Prometheus metrics endpoint
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)
