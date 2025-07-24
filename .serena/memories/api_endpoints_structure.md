# API Endpoints Structure

## Base URL: `/api/v1`

## Authentication Endpoints
- `POST /auth/register` - Create new user (10/hour rate limit)
- `POST /auth/login` - Get JWT token (5/min rate limit)
- `GET /auth/me` - Get current user info

## Todo Endpoints (Auth Required)
- `GET /todos` - List todos with pagination/filtering
  - Query params: limit, offset, status, category_id, search, sort_by, sort_order
- `POST /todos` - Create new todo
- `GET /todos/{todo_id}` - Get specific todo
- `PUT /todos/{todo_id}` - Update todo
- `DELETE /todos/{todo_id}` - Soft delete todo

## Category Endpoints (Auth Required)
- `GET /categories` - List user's categories
- `POST /categories` - Create new category
- `GET /categories/{category_id}` - Get specific category
- `PUT /categories/{category_id}` - Update category
- `DELETE /categories/{category_id}` - Delete category
- `GET /categories/{category_id}/todos` - Get todos in category

## Utility Endpoints
- `GET /` - Root endpoint (redirect to /docs)
- `GET /health` - Health check
- `GET /test-rate-limit` - Test rate limiting

## Documentation
- `/docs` - Swagger UI
- `/redoc` - ReDoc documentation
- `/openapi.json` - OpenAPI schema

## Response Formats
- Success: JSON with data
- Error: `{"detail": "Error message"}`
- Pagination: Includes `total` count with results