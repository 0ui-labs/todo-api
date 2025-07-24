# Todo API

A production-ready REST API for managing todos with JWT authentication, PostgreSQL persistence, and Redis-based rate limiting.

## Features

- RESTful API for todo management
- JWT-based authentication
- PostgreSQL database with Alembic migrations
- Redis-based rate limiting
- Comprehensive test suite
- Docker deployment ready
- OpenAPI/Swagger documentation

## API Documentation

### Base URL
```
http://localhost:8000/api/v1
```

### Authentication
All endpoints except `/auth/register` and `/auth/login` require JWT authentication.

Include the JWT token in the Authorization header:
```
Authorization: Bearer <your-jwt-token>
```

## Rate Limiting

### Overview
The API implements rate limiting to prevent abuse and ensure fair usage. Rate limits are enforced using Redis and are applied per IP address for unauthenticated requests and per user ID for authenticated requests.

### Default Rate Limits
- **General Endpoints**: 100 requests per minute, 1000 requests per hour
- **Authentication Endpoints**:
  - `/auth/login`: 5 requests per minute
  - `/auth/register`: 10 requests per hour

### Rate Limit Headers
Every API response includes rate limit information in the following headers:

| Header | Description |
|--------|-------------|
| `X-RateLimit-Limit` | Maximum number of requests allowed in the current window |
| `X-RateLimit-Remaining` | Number of requests remaining in the current window |
| `X-RateLimit-Reset` | Unix timestamp when the rate limit window resets |

Example response headers:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1627890123
```

### Rate Limit Exceeded Response
When rate limits are exceeded, the API returns a 429 status code with the following response format:

```json
{
  "detail": "Rate limit exceeded. Please retry after 1627890123",
  "retry_after": 1627890123
}
```

The `retry_after` field contains the Unix timestamp indicating when the client can retry the request.

### Redis Configuration
Rate limiting requires Redis to be running. Configuration options can be set via environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `REDIS_URL` | Redis connection URL | `redis://localhost:6379/0` |
| `RATE_LIMIT_ENABLED` | Enable/disable rate limiting | `true` |
| `RATE_LIMIT_PER_MINUTE` | Default requests per minute | `100` |
| `RATE_LIMIT_PER_HOUR` | Default requests per hour | `1000` |

To disable rate limiting (not recommended for production):
```bash
export RATE_LIMIT_ENABLED=false
```

## Endpoints

### Authentication

#### Register
```
POST /auth/register
```
Create a new user account.

**Rate Limit**: 10 requests per hour

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "securepassword",
  "full_name": "John Doe"
}
```

#### Login
```
POST /auth/login
```
Authenticate and receive a JWT token.

**Rate Limit**: 5 requests per minute

**Request Body**:
```json
{
  "username": "user@example.com",
  "password": "securepassword"
}
```

### Todos

All todo endpoints require authentication and are subject to the default rate limits (100/min, 1000/hour).

#### List Todos
```
GET /todos
```
Retrieve all todos for the authenticated user.

#### Create Todo
```
POST /todos
```
Create a new todo.

#### Get Todo
```
GET /todos/{todo_id}
```
Retrieve a specific todo.

#### Update Todo
```
PUT /todos/{todo_id}
```
Update an existing todo.

#### Delete Todo
```
DELETE /todos/{todo_id}
```
Delete a todo.

### Categories

All category endpoints require authentication and are subject to the default rate limits (100/min, 1000/hour).

#### List Categories
```
GET /categories
```
Retrieve all categories for the authenticated user.

#### Create Category
```
POST /categories
```
Create a new category.

## Installation

### Using Docker (Recommended)

1. Clone the repository
2. Navigate to the docker directory:
   ```bash
   cd todo-api/docker
   ```
3. Start the services:
   ```bash
   docker-compose up
   ```

This will start:
- PostgreSQL database
- Redis server
- Todo API application

### Manual Installation

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. Run database migrations:
   ```bash
   alembic upgrade head
   ```

4. Start the application:
   ```bash
   uvicorn app.main:app --reload
   ```

## Testing

Run the test suite:
```bash
pytest tests/ -v
```

With coverage:
```bash
pytest tests/ -v --cov=app --cov-report=html
```

## API Documentation

Interactive API documentation is available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- OpenAPI Schema: http://localhost:8000/openapi.json

## Error Responses

The API uses standard HTTP status codes and returns errors in the following format:

```json
{
  "detail": "Error message description"
}
```

Common status codes:
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `422` - Validation Error
- `429` - Too Many Requests (Rate Limit Exceeded)
- `500` - Internal Server Error