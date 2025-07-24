# Development Commands

## Installation
```bash
pip install -e .  # Install with pyproject.toml
```

## Database Setup
```bash
cp .env.example .env  # Copy environment template
# Edit .env with database credentials
alembic upgrade head  # Run migrations
alembic revision --autogenerate -m "Description"  # Create new migration
```

## Development Server
```bash
uvicorn app.main:app --reload  # Development with auto-reload
uvicorn app.main:app  # Production server
```

## Testing
```bash
pytest tests/ -v  # Run all tests
pytest tests/ -v --cov=app --cov-report=html  # With coverage report
pytest tests/unit/test_todo_service.py -v  # Run specific test file
pytest tests/unit/test_todo_service.py::test_create_todo -v  # Run specific test
```

## Code Quality
```bash
ruff check .  # Linting
ruff check . --fix  # Auto-fix linting issues
mypy app/  # Type checking
```

## Docker Development
```bash
cd docker && docker-compose up  # Start all services
docker-compose up --build  # Rebuild after changes
```

## System Commands (Darwin/macOS)
- Standard Unix commands work: git, ls, cd, grep, find
- Use `lsof -ti:8000 | xargs kill -9` to kill process on port 8000