"""Authentication middleware."""
import logging
from collections.abc import Awaitable, Callable

from fastapi import Request
from fastapi.security.utils import get_authorization_scheme_param
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

logger = logging.getLogger(__name__)


class AuthMiddleware(BaseHTTPMiddleware):
    """Middleware to handle authentication headers and logging."""

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        """Process the request and add authentication logging."""
        # Extract authorization header
        authorization = request.headers.get("Authorization")

        if authorization:
            scheme, param = get_authorization_scheme_param(authorization)
            if scheme.lower() == "bearer":
                # Log authenticated request (without exposing the token)
                logger.debug(
                    f"Authenticated request to {request.url.path} "
                    f"[Method: {request.method}]"
                )
            else:
                logger.warning(
                    f"Invalid authentication scheme: {scheme} "
                    f"[Path: {request.url.path}]"
                )

        # Process request
        response = await call_next(request)

        return response
