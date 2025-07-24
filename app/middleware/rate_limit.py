# Configure logging
import logging

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


# Create Limiter instance
limiter = Limiter(
    key_func=get_rate_limit_key,
    default_limits=[
        f"{settings.rate_limit_per_minute}/minute",
        f"{settings.rate_limit_per_hour}/hour"
    ],
    storage_uri=settings.redis_url if settings.redis_url else None,
    headers_enabled=True,
    in_memory_fallback_enabled=True,
)

# Custom Error Handler for 429 Responses
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
