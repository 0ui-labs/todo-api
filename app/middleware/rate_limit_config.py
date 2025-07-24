"""Rate limiting configuration for different endpoints."""



class RateLimitConfig:
    """Centralized rate limit configuration."""

    # Authentication endpoints - more restrictive
    AUTH_LIMITS = {
        "register": "10/hour",  # Prevent spam registrations
        "login": "5/minute",    # Prevent brute force
        "refresh": "10/minute", # Token refresh
        "logout": "10/minute",  # Logout operations
    }

    # Todo endpoints - balanced limits
    TODO_LIMITS = {
        "create": "30/minute",   # Create new todos
        "list": "60/minute",     # List todos (read-heavy)
        "get": "100/minute",     # Get single todo
        "update": "30/minute",   # Update todo
        "delete": "20/minute",   # Delete todo (more restrictive)
        "bulk": "5/minute",      # Bulk operations
    }

    # Category endpoints
    CATEGORY_LIMITS = {
        "create": "20/minute",   # Create category
        "list": "60/minute",     # List categories
        "get": "60/minute",      # Get single category
        "update": "20/minute",   # Update category
        "delete": "10/minute",   # Delete category (most restrictive)
    }

    # Tag endpoints - least restrictive
    TAG_LIMITS = {
        "create": "50/minute",   # Create tag
        "list": "100/minute",    # List tags
        "update": "50/minute",   # Update tag
        "delete": "30/minute",   # Delete tag
    }

    # Special limits for admin operations
    ADMIN_LIMITS = {
        "default": "10/minute",  # Admin operations
    }

    # Different limits for authenticated vs unauthenticated users
    UNAUTHENTICATED_LIMITS = {
        "default": "20/minute",  # More restrictive for anonymous users
        "strict": "5/minute",    # Very restrictive endpoints
    }

    @classmethod
    def get_all_limits(cls) -> dict[str, dict[str, str]]:
        """Get all configured limits."""
        return {
            "auth": cls.AUTH_LIMITS,
            "todos": cls.TODO_LIMITS,
            "categories": cls.CATEGORY_LIMITS,
            "tags": cls.TAG_LIMITS,
            "admin": cls.ADMIN_LIMITS,
            "unauthenticated": cls.UNAUTHENTICATED_LIMITS,
        }
