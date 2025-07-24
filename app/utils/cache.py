"""Cache utilities and decorators."""
import functools
import inspect
from collections.abc import Callable

from app.services.cache import get_cache_service


def _make_serializable(obj):
    """Convert SQLAlchemy models and other objects to serializable format."""
    if isinstance(obj, list):
        return [_make_serializable(item) for item in obj]
    elif isinstance(obj, tuple):
        # Handle tuples like (list[Todo], int) from get_todos
        return tuple(_make_serializable(item) for item in obj)
    elif hasattr(obj, '__dict__') and hasattr(obj, '__tablename__'):
        # SQLAlchemy model - convert to dict
        result = {}
        for key, value in obj.__dict__.items():
            if not key.startswith('_'):
                result[key] = _make_serializable(value)
        return result
    elif isinstance(obj, dict | str | int | float | bool | type(None)):
        return obj
    else:
        # Try to convert to string for other types
        return str(obj)


def cache_result(
    namespace: str,
    ttl: int = 300,
    key_prefix: str = "",
    include_user: bool = True
):
    """Decorator to cache async function results.

    Args:
        namespace: Cache namespace (e.g., 'todos', 'categories')
        ttl: Time to live in seconds (default: 5 minutes)
        key_prefix: Optional prefix for cache key
        include_user: Include user_id in cache key if available

    Example:
        @cache_result("todos", ttl=600)
        async def get_user_todos(user_id: str, **filters):
            # Expensive operation
            return todos
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            cache = await get_cache_service()

            # Build cache key from function arguments
            key_parts = [key_prefix] if key_prefix else []

            # Get function signature to map args to parameter names
            sig = inspect.signature(func)
            bound_args = sig.bind(*args, **kwargs)
            bound_args.apply_defaults()

            # Include user_id if available and requested
            if include_user and 'user_id' in bound_args.arguments:
                key_parts.append(f"user:{bound_args.arguments['user_id']}")

            # Add function name
            key_parts.append(func.__name__)

            # Add other arguments (excluding user_id if already included)
            for param_name, value in bound_args.arguments.items():
                if param_name == 'self' or (param_name == 'user_id' and include_user):
                    continue
                # Skip complex objects (like database sessions)
                if param_name in ['db', 'session', 'redis']:
                    continue
                key_parts.append(f"{param_name}:{value}")

            cache_key = ":".join(str(part) for part in key_parts)

            # Try to get from cache
            cached_value = await cache.get(namespace, cache_key)
            if cached_value is not None:
                return cached_value

            # Call the original function
            result = await func(*args, **kwargs)

            # Serialize the result for caching
            serializable_result = _make_serializable(result)

            # Cache the result
            await cache.set(namespace, cache_key, serializable_result, ttl)

            return result

        return wrapper
    return decorator


def invalidate_cache(namespace: str, pattern: str = "*"):
    """Decorator to invalidate cache after function execution.

    Args:
        namespace: Cache namespace to invalidate
        pattern: Pattern to match for invalidation

    Example:
        @invalidate_cache("todos", pattern="user:{user_id}:*")
        async def update_todo(user_id: str, todo_id: str, data: dict):
            # Update operation
            return updated_todo
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            # Execute the function first
            result = await func(*args, **kwargs)

            # Then invalidate cache
            cache = await get_cache_service()

            # Get function signature to extract user_id
            sig = inspect.signature(func)
            bound_args = sig.bind(*args, **kwargs)
            bound_args.apply_defaults()

            # Replace placeholders in pattern
            actual_pattern = pattern
            for param_name, value in bound_args.arguments.items():
                placeholder = f"{{{param_name}}}"
                if placeholder in actual_pattern:
                    actual_pattern = actual_pattern.replace(placeholder, str(value))

            await cache.delete_pattern(namespace, actual_pattern)

            return result

        return wrapper
    return decorator
