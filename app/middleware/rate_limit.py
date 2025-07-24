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
from app.middleware.rate_limit_config import RateLimitConfig
from app.middleware.rate_limit_env_config import EnvRateLimitConfig

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

def get_user_tier(request: Request) -> str | None:
    """Extract user tier from JWT token for tier-based rate limiting."""
    try:
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return None

        token = auth_header.split(" ")[1]
        payload = jwt.decode(
            token,
            settings.secret_key.get_secret_value(),
            algorithms=[settings.algorithm]
        )

        # Check for user tier in token (could be added during login)
        return payload.get("tier", "basic")

    except (JWTError, KeyError, AttributeError):
        return None


def create_endpoint_limiter(
    limit: str,
    key_func: Callable | None = None,
    per_tier: dict[str, str] | None = None
) -> Callable:
    """
    Create a rate limiter for a specific endpoint with optional tier-based limits.
    
    Args:
        limit: Default rate limit string (e.g., "10/minute")
        key_func: Optional custom key function
        per_tier: Optional dict of tier-specific limits {"premium": "100/minute", "admin": "unlimited"}
    """
    # TODO: Fix tier-based rate limiting - currently disabled due to SlowAPI compatibility issue
    # The tier-aware callable is not being called correctly by SlowAPI
    # For now, just use the default limit for all users
    if per_tier:
        # Log a warning that tier-based limiting is not yet implemented
        import logging
        logging.getLogger(__name__).warning(
            "Tier-based rate limiting is not yet implemented, using default limit"
        )

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
    strategy=EnvRateLimitConfig.get_strategy(),  # Configurable strategy
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
    """Centralized rate limiters for all endpoints."""

    # Auth endpoints
    auth_register = create_endpoint_limiter(
        EnvRateLimitConfig.get_limit("AUTH", "REGISTER", RateLimitConfig.AUTH_LIMITS["register"]),
        per_tier=EnvRateLimitConfig.get_tier_limits("AUTH", "REGISTER") or {"admin": "unlimited"}
    )
    auth_login = create_endpoint_limiter(
        EnvRateLimitConfig.get_limit("AUTH", "LOGIN", RateLimitConfig.AUTH_LIMITS["login"]),
        per_tier=EnvRateLimitConfig.get_tier_limits("AUTH", "LOGIN")
    )

    # Todo endpoints with tier support
    todo_create = create_endpoint_limiter(
        EnvRateLimitConfig.get_limit("TODO", "CREATE", RateLimitConfig.TODO_LIMITS["create"]),
        per_tier=EnvRateLimitConfig.get_tier_limits("TODO", "CREATE") or {"premium": "60/minute", "admin": "unlimited"}
    )
    todo_list = create_endpoint_limiter(
        EnvRateLimitConfig.get_limit("TODO", "LIST", RateLimitConfig.TODO_LIMITS["list"]),
        per_tier=EnvRateLimitConfig.get_tier_limits("TODO", "LIST") or {"premium": "120/minute", "admin": "unlimited"}
    )
    todo_get = create_endpoint_limiter(
        EnvRateLimitConfig.get_limit("TODO", "GET", RateLimitConfig.TODO_LIMITS["get"]),
        per_tier=EnvRateLimitConfig.get_tier_limits("TODO", "GET")
    )
    todo_update = create_endpoint_limiter(
        EnvRateLimitConfig.get_limit("TODO", "UPDATE", RateLimitConfig.TODO_LIMITS["update"]),
        per_tier=EnvRateLimitConfig.get_tier_limits("TODO", "UPDATE")
    )
    todo_delete = create_endpoint_limiter(
        EnvRateLimitConfig.get_limit("TODO", "DELETE", RateLimitConfig.TODO_LIMITS["delete"]),
        per_tier=EnvRateLimitConfig.get_tier_limits("TODO", "DELETE")
    )
    todo_bulk = create_endpoint_limiter(
        EnvRateLimitConfig.get_limit("TODO", "BULK", RateLimitConfig.TODO_LIMITS["bulk"]),
        per_tier=EnvRateLimitConfig.get_tier_limits("TODO", "BULK") or {"premium": "10/minute", "admin": "20/minute"}
    )

    # Category endpoints
    category_create = create_endpoint_limiter(
        EnvRateLimitConfig.get_limit("CATEGORY", "CREATE", RateLimitConfig.CATEGORY_LIMITS["create"]),
        per_tier=EnvRateLimitConfig.get_tier_limits("CATEGORY", "CREATE")
    )
    category_list = create_endpoint_limiter(
        EnvRateLimitConfig.get_limit("CATEGORY", "LIST", RateLimitConfig.CATEGORY_LIMITS["list"]),
        per_tier=EnvRateLimitConfig.get_tier_limits("CATEGORY", "LIST")
    )
    category_get = create_endpoint_limiter(
        EnvRateLimitConfig.get_limit("CATEGORY", "GET", RateLimitConfig.CATEGORY_LIMITS["get"]),
        per_tier=EnvRateLimitConfig.get_tier_limits("CATEGORY", "GET")
    )
    category_update = create_endpoint_limiter(
        EnvRateLimitConfig.get_limit("CATEGORY", "UPDATE", RateLimitConfig.CATEGORY_LIMITS["update"]),
        per_tier=EnvRateLimitConfig.get_tier_limits("CATEGORY", "UPDATE")
    )
    category_delete = create_endpoint_limiter(
        EnvRateLimitConfig.get_limit("CATEGORY", "DELETE", RateLimitConfig.CATEGORY_LIMITS["delete"]),
        per_tier=EnvRateLimitConfig.get_tier_limits("CATEGORY", "DELETE")
    )

    # Tag endpoints
    tag_create = create_endpoint_limiter(
        EnvRateLimitConfig.get_limit("TAG", "CREATE", RateLimitConfig.TAG_LIMITS["create"]),
        per_tier=EnvRateLimitConfig.get_tier_limits("TAG", "CREATE")
    )
    tag_list = create_endpoint_limiter(
        EnvRateLimitConfig.get_limit("TAG", "LIST", RateLimitConfig.TAG_LIMITS["list"]),
        per_tier=EnvRateLimitConfig.get_tier_limits("TAG", "LIST")
    )
    tag_update = create_endpoint_limiter(
        EnvRateLimitConfig.get_limit("TAG", "UPDATE", RateLimitConfig.TAG_LIMITS["update"]),
        per_tier=EnvRateLimitConfig.get_tier_limits("TAG", "UPDATE")
    )
    tag_delete = create_endpoint_limiter(
        EnvRateLimitConfig.get_limit("TAG", "DELETE", RateLimitConfig.TAG_LIMITS["delete"]),
        per_tier=EnvRateLimitConfig.get_tier_limits("TAG", "DELETE")
    )
    
    # Admin endpoints
    admin_list = create_endpoint_limiter(
        EnvRateLimitConfig.get_limit("ADMIN", "LIST", "60/minute"),
        per_tier=EnvRateLimitConfig.get_tier_limits("ADMIN", "LIST") or {"admin": "unlimited"}
    )
    admin_action = create_endpoint_limiter(
        EnvRateLimitConfig.get_limit("ADMIN", "ACTION", "30/minute"),
        per_tier=EnvRateLimitConfig.get_tier_limits("ADMIN", "ACTION") or {"admin": "unlimited"}
    )

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
    if not EnvRateLimitConfig.is_enabled():
        logger.info("Rate limiting is disabled via environment configuration")
        return

    # Add rate limit exceeded handler
    app.add_exception_handler(RateLimitExceeded, custom_rate_limit_exceeded_handler)

    # Add middleware for better performance
    app.add_middleware(SlowAPIMiddleware)

    # Store limiter in app state for access in routes
    app.state.limiter = limiter

    # Log configuration
    strategy = EnvRateLimitConfig.get_strategy()
    burst_config = EnvRateLimitConfig.get_burst_config()
    logger.info(
        f"Rate limiting configured successfully - "
        f"Strategy: {strategy}, "
        f"Burst size: {burst_config['size']}"
    )
