"""Main FastAPI application."""
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import make_asgi_app
from slowapi.middleware import SlowAPIMiddleware

from app.api import admin, auth, categories, tags, todos
from app.config import settings
from app.database import engine
from app.middleware.rate_limit import limiter, setup_rate_limiting

# Configure structured logging
from app.monitoring.logging_config import get_logger, setup_logging
from app.monitoring.telemetry import instrument_app, setup_telemetry
from app.redis import close_redis_pools

# Setup logging before anything else
setup_logging(
    level=settings.log_level if hasattr(settings, 'log_level') else "INFO",
    json_logs=settings.json_logs if hasattr(settings, 'json_logs') else True,
    service_name=settings.app_name
)
logger = get_logger(__name__)


def verify_production_config() -> bool:
    """Verify critical production settings."""
    checks = {
        "SECRET_KEY": bool(settings.secret_key),
        "DATABASE_URL": bool(settings.database_url),
        "CORS_ORIGINS": settings.backend_cors_origins != ["*"],
    }

    failed = [k for k, v in checks.items() if not v]
    if failed:
        logger.error(f"Production config missing: {', '.join(failed)}")
        return False

    return True

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Enhanced lifecycle with security checks."""
    logger.info("Starting up Todo API...")

    # Security validation
    if settings.environment == "production":
        if not verify_production_config():
            logger.critical("Production configuration validation failed!")
            raise SystemExit(1)

    # Setup OpenTelemetry
    setup_telemetry(
        service_name="todo-api",
        service_version="1.0.0",
        otlp_endpoint=settings.otlp_endpoint if hasattr(settings, 'otlp_endpoint') else None
    )

    # Instrument the application
    instrument_app(app, engine.sync_engine)

    # Setup database metrics collection
    from app.monitoring.db_metrics import setup_db_metrics
    setup_db_metrics(engine)

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

# Apply custom middleware via registry
from app.middleware.registry import create_middleware_registry

middleware_registry = create_middleware_registry()
middleware_registry.apply_to_app(app)

# SlowAPI middleware is already added in setup_rate_limiting()




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
