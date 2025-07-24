"""Global error handler middleware."""
import logging
from collections.abc import Awaitable, Callable

from fastapi import Request, Response, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)


class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    """Middleware to handle all exceptions globally."""

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        """Process the request and handle any exceptions."""
        try:
            response = await call_next(request)
            return response
        except StarletteHTTPException as exc:
            # Handle HTTP exceptions
            logger.warning(
                f"HTTP exception: {exc.status_code} - {exc.detail} "
                f"[Path: {request.url.path}]"
            )
            return JSONResponse(
                status_code=exc.status_code,
                content={
                    "error": {
                        "message": exc.detail,
                        "type": "http_exception",
                        "status_code": exc.status_code,
                    }
                },
            )
        except RequestValidationError as exc:
            # Handle validation errors
            logger.warning(
                f"Validation error: {exc.errors()} [Path: {request.url.path}]"
            )
            return JSONResponse(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                content={
                    "error": {
                        "message": "Validation failed",
                        "type": "validation_error",
                        "details": exc.errors(),
                    }
                },
            )
        except Exception as exc:
            # Handle all other exceptions
            logger.error(
                f"Unhandled exception: {type(exc).__name__}: {str(exc)} "
                f"[Path: {request.url.path}]",
                exc_info=True,
            )
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "error": {
                        "message": "Internal server error",
                        "type": "internal_error",
                    }
                },
            )
