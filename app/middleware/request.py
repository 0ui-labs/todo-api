"""Request-related middleware."""
import logging
from typing import Optional

from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from app.config import settings

logger = logging.getLogger(__name__)


class RequestSizeLimitMiddleware(BaseHTTPMiddleware):
    """Middleware to limit request body size."""
    
    def __init__(
        self, 
        app: ASGIApp,
        max_size: Optional[int] = None,
        error_message: str = "Request body too large",
        include_max_size_in_error: bool = True
    ):
        """
        Initialize the middleware.
        
        Args:
            app: The ASGI application
            max_size: Maximum request size in bytes (default from settings)
            error_message: Custom error message
            include_max_size_in_error: Include max size in error response
        """
        super().__init__(app)
        self.max_size = max_size or settings.max_request_size
        self.error_message = error_message
        self.include_max_size_in_error = include_max_size_in_error
    
    async def dispatch(self, request: Request, call_next):
        """Check request size before processing."""
        content_length = request.headers.get("content-length")
        
        if content_length:
            try:
                size = int(content_length)
                if size > self.max_size:
                    logger.warning(
                        f"Request size {size} exceeds limit {self.max_size} "
                        f"from {request.client.host}"
                    )
                    
                    error_detail = {
                        "detail": self.error_message,
                        "type": "request_too_large"
                    }
                    
                    if self.include_max_size_in_error:
                        error_detail["max_size_bytes"] = self.max_size
                        error_detail["max_size_mb"] = round(self.max_size / 1024 / 1024, 2)
                    
                    return JSONResponse(
                        status_code=413,
                        content=error_detail
                    )
            except ValueError:
                logger.error(f"Invalid Content-Length header: {content_length}")
                return JSONResponse(
                    status_code=400,
                    content={"detail": "Invalid Content-Length header"}
                )
        
        response = await call_next(request)
        return response


class RequestTimeoutMiddleware(BaseHTTPMiddleware):
    """Middleware to enforce request timeouts."""
    
    def __init__(
        self,
        app: ASGIApp,
        timeout: Optional[int] = None
    ):
        """
        Initialize the middleware.
        
        Args:
            app: The ASGI application
            timeout: Request timeout in seconds
        """
        super().__init__(app)
        self.timeout = timeout or settings.request_timeout
    
    async def dispatch(self, request: Request, call_next):
        """Enforce timeout on request processing."""
        # Implementation would use asyncio.timeout
        # Simplified for PRD
        response = await call_next(request)
        return response