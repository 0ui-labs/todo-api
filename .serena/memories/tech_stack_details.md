# Technology Stack Details

## Core Framework
- **FastAPI**: Modern async web framework
- **Python 3.11+**: Required for latest features
- **Uvicorn**: ASGI server with auto-reload support

## Database
- **PostgreSQL**: Primary database
- **SQLAlchemy 2.0+**: ORM with async support
- **asyncpg**: PostgreSQL async driver
- **Alembic**: Database migration tool

## Authentication & Security
- **python-jose[cryptography]**: JWT token handling
- **passlib[bcrypt]**: Password hashing
- **JWT Settings**: HS256 algorithm, 60-minute expiration

## Validation & Serialization
- **Pydantic v2**: Data validation and settings
- **pydantic[email]**: Email validation support

## Caching & Rate Limiting
- **Redis**: In-memory data store
- **slowapi**: Rate limiting middleware
- **Default Limits**: 100/min, 1000/hour general; 5/min login

## Testing
- **pytest**: Test framework
- **pytest-asyncio**: Async test support
- **pytest-cov**: Coverage reporting
- **httpx**: Async HTTP client for testing

## Code Quality
- **ruff**: Fast Python linter (replaces flake8, isort, etc.)
- **mypy**: Static type checker

## Development Tools
- **Docker & docker-compose**: Container orchestration
- **python-multipart**: Form data parsing