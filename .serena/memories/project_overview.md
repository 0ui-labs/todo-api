# Todo API Project Overview

## Purpose
A production-ready REST API for managing todos with the following features:
- JWT-based authentication
- PostgreSQL database with async support
- Redis-based rate limiting
- Hierarchical categories for todos
- Comprehensive test suite
- Docker deployment ready
- OpenAPI/Swagger documentation

## Architecture
- **Framework**: FastAPI with Python 3.11+
- **Database**: PostgreSQL with SQLAlchemy ORM (async)
- **Caching/Rate Limiting**: Redis with slowapi
- **Authentication**: JWT with python-jose
- **API Version**: /api/v1

## Project Structure
```
app/
├── api/           # API route handlers (controllers)
├── services/      # Business logic layer
├── models/        # SQLAlchemy database models
├── schemas/       # Pydantic schemas for validation
├── middleware/    # Custom middleware (auth, rate limiting, logging)
├── dependencies/  # FastAPI dependency injection
├── utils/         # Utility functions
└── config.py      # Application configuration
```

## Key Patterns
- **Layered Architecture**: Clear separation between API, service, and data layers
- **Dependency Injection**: Used for database sessions, auth, pagination
- **Soft Deletes**: All models have deleted_at field
- **Service Layer**: Business logic in service classes (TodoService, CategoryService, AuthService)
- **Error Handling**: Centralized through ErrorHandlerMiddleware
- **Rate Limiting**: Configurable per endpoint (default: 100/min, 1000/hour)