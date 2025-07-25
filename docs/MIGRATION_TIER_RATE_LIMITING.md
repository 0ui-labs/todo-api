# Migration Guide: Tier-based Rate Limiting Removal

This guide helps developers understand and adapt to the removal of tier-based rate limiting from the Todo API.

## Overview

As of this update, the Todo API has removed tier-based rate limiting in favor of a simpler, uniform rate limiting system. All users now have the same rate limits regardless of any user type or tier.

## What Changed

### Removed Features
- `get_user_tier()` function
- `per_tier` parameter in `create_endpoint_limiter()`
- Tier-specific environment variables (e.g., `RATE_LIMIT_TODO_CREATE_PREMIUM`)
- RateLimitConfig and EnvRateLimitConfig modules

### Simplified Features
- All rate limiters now use simple, uniform limits
- Configuration is straightforward with no tier logic
- Environment variables are cleaner and easier to understand

## Migration Steps

### 1. Remove Tier-Specific Configuration

**Before:**
```bash
RATE_LIMIT_TODO_CREATE=30/minute
RATE_LIMIT_TODO_CREATE_PREMIUM=60/minute
RATE_LIMIT_TODO_CREATE_ADMIN=unlimited
```

**After:**
```bash
RATE_LIMIT_TODO_CREATE=30/minute
```

### 2. Update Client Applications

If your client application was expecting different rate limits for different user types, update it to handle uniform limits:

```python
# Remove any tier-based logic
# Before:
if user.tier == "premium":
    expected_limit = 60
else:
    expected_limit = 30

# After:
expected_limit = 30  # Same for all users
```

### 3. Update Monitoring and Alerting

Update any monitoring dashboards or alerts that were tracking tier-specific metrics.

## Future Considerations

If tier-based rate limiting is needed in the future, it should be implemented properly:

1. Add `tier` field to User model in database
2. Include tier in JWT claims during authentication
3. Implement tier-aware rate limiting logic
4. Add comprehensive tests for tier functionality

## Benefits of This Change

1. **Simplicity**: Easier to understand and maintain
2. **Reliability**: No broken tier logic to debug
3. **Performance**: Slightly faster without tier checks
4. **Clean Code**: Follows YAGNI principle

## Questions?

If you have questions about this migration, please:
1. Check the [Rate Limiting Guide](./RATE-LIMITING.md)
2. Review the implementation in `app/middleware/rate_limit.py`
3. Contact the development team