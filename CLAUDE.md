# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with the Todo API repository.

## Table of Contents

- [Project Overview](#project-overview)
- [Quick Start](#quick-start)
- [Development Commands](#development-commands)
- [Architecture Overview](#architecture-overview)
- [Key Patterns](#key-patterns)
- [Testing](#testing)
- [Additional Documentation](#additional-documentation)
- [Task Processing Hook](#task-processing-hook)

## Project Overview

A production-ready REST API for todo management built with FastAPI, featuring:
- JWT authentication with python-jose
- PostgreSQL database with async SQLAlchemy
- Redis-based rate limiting
- Hierarchical categories
- Comprehensive test coverage
- Docker deployment ready
- Auto-generated OpenAPI documentation

## Quick Start

```bash
# Setup environment
cp .env.example .env
# Edit .env with your database credentials

# Install dependencies
pip install -e .

# Run database migrations
alembic upgrade head

# Start development server
uvicorn app.main:app --reload
```

## Development Commands

### Server Management
- **Development**: `uvicorn app.main:app --reload`
- **Production**: `uvicorn app.main:app`
- **Docker**: `cd docker && docker-compose up`

### Database Operations
- **Run migrations**: `alembic upgrade head`
- **Create migration**: `alembic revision --autogenerate -m "Description"`
- **Rollback**: `alembic downgrade -1`

### Testing
- **All tests**: `pytest tests/ -v`
- **With coverage**: `pytest tests/ -v --cov=app --cov-report=html`
- **Specific file**: `pytest tests/unit/test_todo_service.py -v`

### Code Quality
- **Linting**: `ruff check .`
- **Auto-fix**: `ruff check . --fix`
- **Type checking**: `mypy app/`

## Architecture Overview

```
app/
├── api/           # Route handlers (controllers)
├── services/      # Business logic layer
├── models/        # SQLAlchemy models
├── schemas/       # Pydantic schemas
├── middleware/    # Auth, rate limiting, logging
├── dependencies/  # FastAPI dependency injection
├── utils/         # Utility functions
└── config.py      # Application configuration
```

### Technology Stack
- **Framework**: FastAPI with Python 3.11+
- **Database**: PostgreSQL (async SQLAlchemy)
- **Cache/Rate Limit**: Redis with slowapi
- **Auth**: JWT with python-jose
- **Validation**: Pydantic v2
- **Testing**: pytest with pytest-asyncio
- **Code Quality**: ruff, mypy

## Key Patterns

### API Design
- RESTful endpoints: `/api/v1/{resource}`
- Standard HTTP methods and status codes
- Pagination with `limit` and `offset`
- Filtering and sorting support

### Dependency Injection
```python
# Common dependencies
DatabaseSession  # Async DB session
CurrentUser     # Authenticated user
PaginationParams # Pagination helpers
```

### Service Layer
- `TodoService`: Todo CRUD operations
- `CategoryService`: Category management  
- `AuthService`: Authentication/users

### Database Patterns
- Soft deletes with `deleted_at` field
- UUID primary keys
- Automatic timestamps
- Relationship mappings

### Security
- JWT Bearer authentication
- Bcrypt password hashing
- CORS configuration
- Security headers middleware
- Rate limiting per endpoint

## Testing

### Test Structure
```
tests/
├── unit/        # Service layer tests
├── integration/ # API endpoint tests
└── conftest.py  # Shared fixtures
```

### Key Fixtures
- `test_client`: Async HTTP client
- `test_user`: Authenticated user with token
- `db_session`: Test database session

### Running Tests
```bash
# Quick test of specific functionality
pytest tests/unit/test_todo_service.py::test_create_todo -v

# Full test suite with coverage
pytest tests/ -v --cov=app --cov-report=html
```

## Additional Documentation

For more detailed information, see:
- **[Python Development Guide](docs/PYTHON-GUIDE.md)** - Coding standards, patterns, and best practices
- **[PRP Framework](docs/PRP-FRAMEWORK.md)** - Product Requirement Prompt methodology
- **[API Documentation](http://localhost:8000/docs)** - Interactive Swagger UI (when server is running)

## Important Notes

- Always run linting/type checking before committing
- Write tests for new features  
- Update migrations when changing models
- Use environment variables for configuration
- Follow existing patterns and conventions

## Coding Standards

When implementing features, automatically follow these standards:
- **Code Style**: See [Python Guide](docs/PYTHON-GUIDE.md) - use type hints, max 100 char lines, ruff formatting
- **Testing**: Write tests first (TDD), use pytest fixtures, aim for 80%+ coverage
- **Error Handling**: Create custom exceptions, fail fast, use proper logging
- **PRPs**: For new features, reference [PRP Framework](docs/PRP-FRAMEWORK.md)

## Task Processing Hooks

**IMPORTANT**: Before starting any task, perform intelligent AI analysis:

### 1. AI-Powered Task Analysis (Claude Code Internal)
As Claude Code, analyze each task to determine:
- **Task Classification**: Is this programming, planning, or mixed?
- **Technology Detection**: What technologies are mentioned or implied?
- **Context Requirements**: What documentation is needed?

When analyzing, consider:
- Implicit technology needs (e.g., "user registration" → likely needs auth/JWT)
- Related technologies (e.g., "API" → FastAPI, Pydantic, possibly Redis)
- Task complexity and required guides

### 2. Automatic Documentation Loading
Based on analysis, automatically:
- **Load Context7 docs** for detected technologies:
  - FastAPI → `/tiangolo/fastapi`
  - SQLAlchemy → `/sqlalchemy/sqlalchemy`
  - PostgreSQL → `/postgresql/postgresql`
  - Redis → `/redis/redis`
  - Pydantic → `/pydantic/pydantic`
  - pytest → `/pytest-dev/pytest`
  - JWT → `/python-jose/python-jose`

### 3. Guide Selection
- **Python Guide** (`docs/PYTHON-GUIDE.md`): For any coding tasks
- **PRP Framework** (`docs/PRP-FRAMEWORK.md`): For planning or `/prp-*` commands

### Example Analysis:
Task: "Implement secure user registration"
→ Detect: FastAPI (API), JWT (secure), Pydantic (validation)
→ Load: Context7 docs for all three
→ Apply: Python-Guide for implementation standards

This ensures maximum accuracy through AI understanding, not just keyword matching.