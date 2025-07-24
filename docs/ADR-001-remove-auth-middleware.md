# ADR-001: Remove AuthMiddleware in favor of Dependency-based Auth

## Status
Implemented

## Date
2025-07-25

## Context
The Todo API had an `AuthMiddleware` component that was causing confusion:
- The name suggested it enforced authentication on all routes
- In reality, it only performed logging of authentication headers
- This created false security assumptions for developers
- The logging functionality was redundant with the existing `LoggingMiddleware`
- Authentication was already correctly implemented via FastAPI's dependency injection

## Decision
We decided to completely remove the `AuthMiddleware` component and rely exclusively on FastAPI's dependency injection system for authentication.

## Rationale
1. **Clarity**: Removing the misleading middleware eliminates confusion about how authentication works
2. **Simplicity**: One less middleware component to maintain
3. **Performance**: Slightly improved performance with fewer middleware layers
4. **Consistency**: Aligns with FastAPI best practices of using dependencies for auth
5. **Explicitness**: Each route explicitly declares its authentication requirements

## Implementation
1. Removed `AuthMiddleware` import from `app/main.py`
2. Removed middleware registration from the middleware stack
3. Deleted `app/middleware/auth.py` file
4. Verified that `LoggingMiddleware` already captures user context for authenticated requests
5. Added comprehensive tests to ensure auth functionality remains intact

## Consequences
### Positive
- Clearer architecture without misleading components
- Reduced code complexity
- Better alignment with FastAPI patterns
- Explicit authentication requirements per route
- No more redundant logging

### Negative
- None identified - the middleware was purely redundant

### Neutral
- Developers must ensure each protected route explicitly includes the `CurrentUser` dependency
- Auth logging now solely handled by `LoggingMiddleware`

## Testing
All authentication scenarios were tested and verified:
- Valid token access: ✓
- No token rejection: ✓
- Invalid token rejection: ✓
- Invalid auth schemes rejection: ✓
- Logging preservation: ✓

## References
- [FastAPI Security Documentation](https://fastapi.tiangolo.com/tutorial/security/)
- [PR: Auth Middleware Cleanup](PRPs/planning/auth-middleware-cleanup-prd.md)