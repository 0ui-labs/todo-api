# Rate Limiting Documentation

This document describes the rate limiting implementation for the Todo API, including configuration, usage, and customization options.

## Table of Contents

- [Overview](#overview)
- [Default Limits](#default-limits)
- [Configuration](#configuration)
- [Tier-Based Limits](#tier-based-limits)
- [Response Headers](#response-headers)
- [Error Responses](#error-responses)
- [Testing](#testing)
- [Monitoring](#monitoring)

## Overview

The Todo API implements comprehensive rate limiting to:
- Prevent abuse and ensure fair usage
- Protect against brute force attacks
- Maintain service availability
- Support different user tiers

### Key Features

- **Per-user rate limiting** using JWT tokens (falls back to IP address)
- **Redis-backed storage** with in-memory fallback
- **Moving window strategy** for accurate rate tracking
- **Tier-based limits** for premium users
- **Environment-based configuration**
- **Detailed error responses** with retry information

## Default Limits

### Authentication Endpoints

| Endpoint | Default Limit | Description |
|----------|--------------|-------------|
| POST /auth/register | 10/hour | Prevent spam registrations |
| POST /auth/login | 5/minute | Prevent brute force attacks |
| POST /auth/refresh | 10/minute | Token refresh operations |
| POST /auth/logout | 10/minute | Logout operations |

### Todo Endpoints

| Endpoint | Default Limit | Premium Limit | Admin Limit |
|----------|--------------|---------------|-------------|
| POST /todos | 30/minute | 60/minute | unlimited |
| GET /todos | 60/minute | 120/minute | unlimited |
| GET /todos/{id} | 100/minute | - | - |
| PUT /todos/{id} | 30/minute | - | - |
| DELETE /todos/{id} | 20/minute | - | - |
| POST /todos/bulk | 5/minute | 10/minute | 20/minute |

### Category Endpoints

| Endpoint | Default Limit |
|----------|--------------|
| POST /categories | 20/minute |
| GET /categories | 60/minute |
| GET /categories/{id} | 60/minute |
| PUT /categories/{id} | 20/minute |
| DELETE /categories/{id} | 10/minute |

### Tag Endpoints

| Endpoint | Default Limit |
|----------|--------------|
| POST /tags | 50/minute |
| GET /tags | 100/minute |
| PUT /tags/{id} | 50/minute |
| DELETE /tags/{id} | 30/minute |

## Configuration

### Environment Variables

Rate limits can be configured via environment variables. All settings are optional and will fall back to defaults if not specified.

#### Global Settings

```bash
# Enable/disable rate limiting
RATE_LIMIT_ENABLED=true

# Rate limiting strategy (moving-window, fixed-window)
RATE_LIMIT_STRATEGY=moving-window

# Default global limits
RATE_LIMIT_PER_MINUTE=60
RATE_LIMIT_PER_HOUR=1000

# Burst configuration
RATE_LIMIT_BURST_SIZE=10
RATE_LIMIT_BURST_REFILL_RATE=1
RATE_LIMIT_BURST_REFILL_PERIOD=1
```

#### Endpoint-Specific Limits

Format: `RATE_LIMIT_{CATEGORY}_{OPERATION}`

```bash
# Authentication limits
RATE_LIMIT_AUTH_REGISTER=10/hour
RATE_LIMIT_AUTH_LOGIN=5/minute

# Todo limits
RATE_LIMIT_TODO_CREATE=30/minute
RATE_LIMIT_TODO_LIST=60/minute
RATE_LIMIT_TODO_GET=100/minute
RATE_LIMIT_TODO_UPDATE=30/minute
RATE_LIMIT_TODO_DELETE=20/minute
RATE_LIMIT_TODO_BULK=5/minute

# Category limits
RATE_LIMIT_CATEGORY_CREATE=20/minute
RATE_LIMIT_CATEGORY_LIST=60/minute
RATE_LIMIT_CATEGORY_GET=60/minute
RATE_LIMIT_CATEGORY_UPDATE=20/minute
RATE_LIMIT_CATEGORY_DELETE=10/minute

# Tag limits
RATE_LIMIT_TAG_CREATE=50/minute
RATE_LIMIT_TAG_LIST=100/minute
RATE_LIMIT_TAG_UPDATE=50/minute
RATE_LIMIT_TAG_DELETE=30/minute
```

#### Tier-Specific Limits

Format: `RATE_LIMIT_{CATEGORY}_{OPERATION}_{TIER}`

```bash
# Premium user limits
RATE_LIMIT_TODO_CREATE_PREMIUM=60/minute
RATE_LIMIT_TODO_LIST_PREMIUM=120/minute
RATE_LIMIT_TODO_BULK_PREMIUM=10/minute

# Admin user limits
RATE_LIMIT_AUTH_REGISTER_ADMIN=unlimited
RATE_LIMIT_TODO_CREATE_ADMIN=unlimited
RATE_LIMIT_TODO_LIST_ADMIN=unlimited
RATE_LIMIT_TODO_BULK_ADMIN=20/minute
```

### Redis Configuration

Rate limiting uses Redis for distributed storage:

```bash
REDIS_URL=redis://localhost:6379/1
```

If Redis is unavailable, the system falls back to in-memory storage.

## Tier-Based Limits

The system supports three user tiers:

1. **Basic** (default) - Standard rate limits
2. **Premium** - Higher limits for paid users
3. **Admin** - Highest limits or unlimited access

### Adding Tier Information

To enable tier-based rate limiting, include the `tier` field in JWT tokens:

```python
# During login/token generation
payload = {
    "sub": str(user.id),
    "tier": user.tier,  # "basic", "premium", or "admin"
    "exp": expire
}
token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
```

## Response Headers

All rate-limited endpoints include the following headers:

| Header | Description |
|--------|-------------|
| X-RateLimit-Limit | The rate limit for the current window |
| X-RateLimit-Remaining | Number of requests remaining |
| X-RateLimit-Reset | Unix timestamp when the limit resets |
| Retry-After | Seconds to wait before retrying (only on 429 responses) |

### Example Response Headers

```http
HTTP/1.1 200 OK
X-RateLimit-Limit: 30/minute
X-RateLimit-Remaining: 25
X-RateLimit-Reset: 1704123660
```

## Error Responses

When rate limit is exceeded, the API returns a 429 status code:

```http
HTTP/1.1 429 Too Many Requests
Retry-After: 45
X-RateLimit-Limit: 30/minute
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1704123660
Content-Type: application/json

{
    "detail": "Rate limit exceeded: 30 per 1 minute",
    "error": "rate_limit_exceeded",
    "limit": "30/minute"
}
```

## Testing

### Running Rate Limit Tests

```bash
# Run all rate limiting tests
pytest tests/integration/test_rate_limiting.py -v

# Run specific test
pytest tests/integration/test_rate_limiting.py::TestRateLimiting::test_auth_login_rate_limit -v

# Run with coverage
pytest tests/integration/test_rate_limiting.py -v --cov=app.middleware.rate_limit
```

### Manual Testing

1. **Test basic rate limiting:**
```bash
# Make requests until rate limited
for i in {1..35}; do
  curl -X POST http://localhost:8000/api/v1/todos \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d '{"title": "Test Todo"}'
done
```

2. **Test auth endpoint limits:**
```bash
# Try multiple login attempts
for i in {1..6}; do
  curl -X POST http://localhost:8000/api/v1/auth/login \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "username=test@example.com&password=wrong"
done
```

3. **Check rate limit headers:**
```bash
curl -i -X GET http://localhost:8000/api/v1/todos \
  -H "Authorization: Bearer $TOKEN"
```

## Monitoring

### Logging

Rate limit violations are logged with details:

```python
WARNING - Rate limit exceeded for user:123 - Path: /api/v1/todos - Method: POST - Detail: 30 per 1 minute
```

### Metrics to Monitor

1. **Rate limit hit ratio** - Percentage of requests that hit rate limits
2. **Per-endpoint violations** - Which endpoints hit limits most often
3. **Per-user violations** - Identify potential abuse patterns
4. **Redis performance** - Monitor Redis connection and response times

### Example Monitoring Query (if using structured logging):

```sql
-- Find users hitting rate limits frequently
SELECT 
    user_id,
    COUNT(*) as violation_count,
    MIN(timestamp) as first_violation,
    MAX(timestamp) as last_violation
FROM logs
WHERE level = 'WARNING' 
    AND message LIKE 'Rate limit exceeded%'
    AND timestamp > NOW() - INTERVAL '1 day'
GROUP BY user_id
ORDER BY violation_count DESC;
```

## Best Practices

1. **Set appropriate limits** - Balance between security and usability
2. **Monitor and adjust** - Use metrics to fine-tune limits
3. **Communicate limits** - Document limits in API documentation
4. **Handle 429 responses** - Implement retry logic in clients
5. **Use tiered limits** - Reward premium users with higher limits
6. **Test thoroughly** - Ensure limits work as expected

## Troubleshooting

### Common Issues

1. **Rate limits not working:**
   - Check if `RATE_LIMIT_ENABLED=true`
   - Verify Redis connection
   - Check middleware is properly configured

2. **Wrong limits applied:**
   - Verify environment variables are set correctly
   - Check tier information in JWT tokens
   - Ensure middleware is using correct configuration

3. **Headers missing:**
   - Verify `headers_enabled=True` in limiter configuration
   - Check if response is being modified by other middleware

### Debug Mode

Enable debug logging for rate limiting:

```python
import logging
logging.getLogger("app.middleware.rate_limit").setLevel(logging.DEBUG)
```

This will show detailed information about rate limit calculations and key generation.