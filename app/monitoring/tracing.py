"""Manual tracing utilities for custom spans."""
from collections.abc import Callable
from functools import wraps
from typing import Any

from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode


def trace_async(span_name: str | None = None):
    """Decorator to add tracing to async functions.
    
    Args:
        span_name: Optional custom span name (defaults to function name)
    """
    def decorator(func: Callable) -> Callable:
        tracer = trace.get_tracer(__name__)
        actual_span_name = span_name or func.__name__
        
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            with tracer.start_as_current_span(actual_span_name) as span:
                # Add function arguments as span attributes
                if args:
                    span.set_attribute("args.count", len(args))
                if kwargs:
                    for key, value in kwargs.items():
                        if isinstance(value, (str, int, float, bool)):
                            span.set_attribute(f"arg.{key}", value)
                
                try:
                    result = await func(*args, **kwargs)
                    span.set_status(Status(StatusCode.OK))
                    return result
                except Exception as e:
                    span.set_status(
                        Status(StatusCode.ERROR, str(e))
                    )
                    span.record_exception(e)
                    raise
        
        return wrapper
    return decorator


def trace_sync(span_name: str | None = None):
    """Decorator to add tracing to sync functions.
    
    Args:
        span_name: Optional custom span name (defaults to function name)
    """
    def decorator(func: Callable) -> Callable:
        tracer = trace.get_tracer(__name__)
        actual_span_name = span_name or func.__name__
        
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            with tracer.start_as_current_span(actual_span_name) as span:
                # Add function arguments as span attributes
                if args:
                    span.set_attribute("args.count", len(args))
                if kwargs:
                    for key, value in kwargs.items():
                        if isinstance(value, (str, int, float, bool)):
                            span.set_attribute(f"arg.{key}", value)
                
                try:
                    result = func(*args, **kwargs)
                    span.set_status(Status(StatusCode.OK))
                    return result
                except Exception as e:
                    span.set_status(
                        Status(StatusCode.ERROR, str(e))
                    )
                    span.record_exception(e)
                    raise
        
        return wrapper
    return decorator


def add_span_attributes(**attributes: Any) -> None:
    """Add attributes to the current span.
    
    Args:
        **attributes: Key-value pairs to add as span attributes
    """
    span = trace.get_current_span()
    if span and span.is_recording():
        for key, value in attributes.items():
            if isinstance(value, (str, int, float, bool)):
                span.set_attribute(key, value)


def record_exception(exception: Exception) -> None:
    """Record an exception in the current span.
    
    Args:
        exception: Exception to record
    """
    span = trace.get_current_span()
    if span and span.is_recording():
        span.record_exception(exception)
        span.set_status(Status(StatusCode.ERROR, str(exception)))


def get_trace_id() -> str | None:
    """Get the current trace ID.
    
    Returns:
        Trace ID as hex string or None if not in a trace
    """
    span = trace.get_current_span()
    if span and span.is_recording():
        context = span.get_span_context()
        if context and context.trace_id:
            return format(context.trace_id, '032x')
    return None


def get_span_id() -> str | None:
    """Get the current span ID.
    
    Returns:
        Span ID as hex string or None if not in a span
    """
    span = trace.get_current_span()
    if span and span.is_recording():
        context = span.get_span_context()
        if context and context.span_id:
            return format(context.span_id, '016x')
    return None