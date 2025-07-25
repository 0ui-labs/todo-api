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

## Documentation

- [Python Development Guide](docs/PYTHON-GUIDE.md) - Coding standards and best practices
- [Rate Limiting Guide](docs/RATE-LIMITING.md) - Comprehensive rate limiting documentation
- [PRP Framework](docs/PRP-FRAMEWORK.md) - Product Requirement Prompt methodology

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

The API implements rate limiting to prevent abuse and ensure fair usage.

### Current Limits

All authenticated users have the following limits:

| Endpoint Category | Limit |
|------------------|-------|
| Authentication | 5 requests/minute |
| Todo Operations | 60 requests/minute |
| Bulk Operations | 5 requests/minute |

### Configuration

Rate limits can be configured via environment variables:

```bash
RATE_LIMIT_PER_MINUTE=100
RATE_LIMIT_TODO_CREATE=30/minute
```

For detailed information, see the [Rate Limiting Guide](docs/RATE-LIMITING.md).

**Note**: The API currently uses uniform rate limiting for all users. 
Tier-based limiting may be implemented in future versions.

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

## 🔐 Security Configuration

### SECRET_KEY Setup (Required for Production)

The SECRET_KEY is critical for JWT token security and must meet strict entropy requirements.

**Generate a cryptographically secure key:**
```bash
# Recommended: Use the provided script
python scripts/generate_secret_key.py

# Alternative methods:
# Using Python
python -c "import secrets; print(secrets.token_urlsafe(64))"

# Using OpenSSL
openssl rand -base64 64 | tr -d '
='
```

**Set in environment:**
```bash
# .env file
SECRET_KEY="your-generated-64-character-key"
```

**Production Requirements:**
- Minimum 64 characters length
- Minimum 16 unique characters (entropy check)
- Cryptographically secure random generation
- No weak patterns (repeated chars, dictionary words)
- Unique per environment
- Never commit to git

**⚠️ Security Warning:**
The API now enforces entropy validation. Keys like "aaaa...aaaa" or simple patterns will be rejected even if they meet the length requirement. Always use cryptographically secure random generators.

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