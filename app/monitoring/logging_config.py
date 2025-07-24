"""Structured logging configuration with JSON formatting."""
import json
import logging
import sys
from contextvars import ContextVar
from typing import Any

from pythonjsonlogger import jsonlogger

# Context variables for request correlation
request_id_context: ContextVar[str | None] = ContextVar("request_id", default=None)
user_id_context: ContextVar[str | None] = ContextVar("user_id", default=None)
trace_id_context: ContextVar[str | None] = ContextVar("trace_id", default=None)
span_id_context: ContextVar[str | None] = ContextVar("span_id", default=None)


class ContextFilter(logging.Filter):
    """Filter to add context variables to log records."""
    
    def filter(self, record: logging.LogRecord) -> bool:
        """Add context variables to the log record."""
        record.request_id = request_id_context.get()
        record.user_id = user_id_context.get()
        record.trace_id = trace_id_context.get()
        record.span_id = span_id_context.get()
        return True


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    """Custom JSON formatter with additional fields."""
    
    def add_fields(self, log_record: dict[str, Any], record: logging.LogRecord, message_dict: dict[str, Any]) -> None:
        """Add custom fields to the log record."""
        super().add_fields(log_record, record, message_dict)
        
        # Add timestamp in ISO format
        log_record["timestamp"] = self.formatTime(record, self.datefmt)
        
        # Add severity (uppercase level name)
        log_record["severity"] = record.levelname
        
        # Add logger name
        log_record["logger"] = record.name
        
        # Add source location
        log_record["source"] = {
            "file": record.pathname,
            "line": record.lineno,
            "function": record.funcName
        }
        
        # Add exception info if present
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)
        
        # Remove redundant fields
        for field in ["levelname", "pathname", "lineno", "funcName", "exc_info", "exc_text"]:
            log_record.pop(field, None)


def setup_logging(
    level: str = "INFO",
    json_logs: bool = True,
    service_name: str = "todo-api"
) -> None:
    """Configure structured logging for the application.
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        json_logs: Whether to use JSON formatting
        service_name: Name of the service for log identification
    """
    # Clear existing handlers
    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    
    # Create handler
    handler = logging.StreamHandler(sys.stdout)
    
    if json_logs:
        # JSON formatter for production
        formatter = CustomJsonFormatter(
            "%(timestamp)s %(severity)s %(name)s %(message)s",
            datefmt="%Y-%m-%dT%H:%M:%S.%fZ"
        )
    else:
        # Human-readable formatter for development
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - [%(request_id)s] - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
    
    handler.setFormatter(formatter)
    
    # Add context filter
    handler.addFilter(ContextFilter())
    
    # Configure root logger
    root_logger.addHandler(handler)
    root_logger.setLevel(getattr(logging, level.upper()))
    
    # Set service name as extra field
    logging.LoggerAdapter(root_logger, {"service": service_name})
    
    # Reduce noise from third-party libraries
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    
    # Log startup message
    root_logger.info(
        "Logging configured",
        extra={
            "service": service_name,
            "level": level,
            "json_logs": json_logs
        }
    )


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance with context support.
    
    Args:
        name: Logger name (usually __name__)
        
    Returns:
        Logger instance
    """
    return logging.getLogger(name)