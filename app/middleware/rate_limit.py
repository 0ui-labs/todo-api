# Configure logging
import logging
from collections.abc import Callable

from jose import jwt
from jose.exceptions import JWTError
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from app.config import settings

logger = logging.getLogger(__name__)


def get_rate_limit_key(request: Request) -> str:
    """Extract rate limit key from JWT token or fall back to IP address."""
    try:
        # Get authorization header
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return get_remote_address(request)

        # Extract token
        token = auth_header.split(" ")[1]

        # Decode token and get user ID
        payload = jwt.decode(
            token,
            settings.secret_key.get_secret_value(),
            algorithms=[settings.algorithm]
        )
        user_id = payload.get("sub")

        if user_id:
            return f"user:{user_id}"

    except (JWTError, KeyError, AttributeError):
        pass

    # Fallback to IP address
    return get_remote_address(request)


def create_endpoint_limiter(
    limit: str,
    key_func: Callable | None = None
) -> Callable:
    """
    Create a rate limiter for a specific endpoint.
    
    Args:
        limit: Rate limit string (e.g., "10/minute")
        key_func: Optional custom key function
    """
    return limiter.limit(limit, key_func=key_func or get_rate_limit_key)


# Create Limiter instance
limiter = Limiter(
    key_func=get_rate_limit_key,
    default_limits=[
        f"{settings.rate_limit_per_minute}/minute",
        f"{settings.rate_limit_per_hour}/hour"
    ],
    storage_uri=settings.redis_url if settings.redis_url else None,
    headers_enabled=False,  # Disabled because FastAPI returns models, not Response objects
    in_memory_fallback_enabled=True,
    strategy="moving-window",  # Default strategy
    swallow_errors=False,  # Don't silently fail on Redis errors
)

# Custom Error Handler for 429 Responses
def create_rate_limit_decorator(limit: str):
    """Create a rate limit decorator with the specified limit."""
    def decorator(func):
        return limiter.limit(limit)(func)
    return decorator


# Pre-configured decorators for common use cases
rate_limit_auth = create_rate_limit_decorator("5/minute")
rate_limit_read = create_rate_limit_decorator("100/minute")
rate_limit_write = create_rate_limit_decorator("30/minute")
rate_limit_delete = create_rate_limit_decorator("20/minute")
rate_limit_admin = create_rate_limit_decorator("10/minute")

# Endpoint-specific limiters using configuration
class RateLimiters:
    """Centralized rate limiters for different endpoints."""

    # Authentication endpoints
    auth_register = limiter.limit(
        lambda: settings.rate_limit_auth_register or "10/hour"
    )
    auth_login = limiter.limit(
        lambda: settings.rate_limit_auth_login or "5/minute"
    )

    # Todo endpoints (simplified)
    todo_create = limiter.limit("30/minute")
    todo_list = limiter.limit("60/minute")
    todo_get = limiter.limit("100/minute")
    todo_update = limiter.limit("30/minute")
    todo_delete = limiter.limit("20/minute")
    todo_bulk = limiter.limit("5/minute")

    # Category endpoints
    category_create = limiter.limit("20/minute")
    category_list = limiter.limit("60/minute")
    category_get = limiter.limit("100/minute")
    category_update = limiter.limit("20/minute")
    category_delete = limiter.limit("10/minute")

    # Tag endpoints
    tag_create = limiter.limit("30/minute")
    tag_list = limiter.limit("60/minute")
    tag_update = limiter.limit("30/minute")
    tag_delete = limiter.limit("20/minute")

    # Admin endpoints
    admin_list = limiter.limit("60/minute")
    admin_action = limiter.limit("30/minute")

async def custom_rate_limit_exceeded_handler(
    request: Request, exc: Exception
) -> Response:
    # Extract user info for logging
    user_key = get_rate_limit_key(request)

    if isinstance(exc, RateLimitExceeded):
        # Log rate limit violation
        logger.warning(
            f"Rate limit exceeded for {user_key} - "
            f"Path: {request.url.path} - "
            f"Method: {request.method} - "
            f"Detail: {exc.detail}"
        )

        # Prepare response content with limit info
        content = {
            "detail": f"Rate limit exceeded: {exc.detail}",
            "error": "rate_limit_exceeded"
        }

        # Add limit info if available
        if exc.limit:
            content["limit"] = str(exc.limit.limit)

        response = JSONResponse(
            status_code=429,
            content=content
        )

        # Add Rate Limit Headers
        if hasattr(exc, 'retry_after'):
            response.headers["Retry-After"] = str(exc.retry_after)

        if exc.limit:
            response.headers["X-RateLimit-Limit"] = str(exc.limit.limit)
            response.headers["X-RateLimit-Remaining"] = "0"
            if hasattr(exc.limit, 'reset_at'):
                response.headers["X-RateLimit-Reset"] = str(exc.limit.reset_at)
    else:
        # Log generic rate limit error
        logger.warning(
            f"Rate limit exceeded for {user_key} - "
            f"Path: {request.url.path} - "
            f"Method: {request.method}"
        )

        response = JSONResponse(
            status_code=429,
            content={
                "detail": "Rate limit exceeded",
                "error": "rate_limit_exceeded",
                "limit": "unknown"
            }
        )
    return response

def setup_rate_limiting(app):
    """Setup rate limiting for the FastAPI application."""
    from slowapi.middleware import SlowAPIMiddleware

    # Check if rate limiting is enabled
    if not settings.rate_limit_enabled:
        logger.info("Rate limiting is disabled")
        return

    # Add rate limit exceeded handler
    app.add_exception_handler(RateLimitExceeded, custom_rate_limit_exceeded_handler)

    # Add middleware for better performance
    app.add_middleware(SlowAPIMiddleware)

    # Store limiter in app state for access in routes
    app.state.limiter = limiter

    # Log configuration
    logger.info(
        f"Rate limiting configured successfully - "
        f"Default limits: {settings.rate_limit_per_minute}/min, {settings.rate_limit_per_hour}/hour"
    )
