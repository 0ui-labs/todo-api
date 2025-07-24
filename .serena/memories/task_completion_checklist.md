# Task Completion Checklist

When completing any coding task, ensure you:

## 1. Code Quality Checks
```bash
ruff check .  # Run linting
ruff check . --fix  # Fix any auto-fixable issues
mypy app/  # Ensure type checking passes
```

## 2. Testing
```bash
pytest tests/ -v  # Run all tests to ensure nothing is broken
# If you added new functionality, write corresponding tests
```

## 3. Database Migrations
If you modified any models:
```bash
alembic revision --autogenerate -m "Description of changes"
alembic upgrade head  # Apply the migration
```

## 4. Documentation
- Update docstrings for new/modified functions
- API endpoints automatically documented via FastAPI
- Update README.md if adding major features

## 5. Environment Variables
- If adding new config, update .env.example
- Document any new environment variables

## 6. Before Committing
- Ensure all tests pass
- Code passes linting and type checking
- No hardcoded secrets or credentials
- Follow existing code patterns and conventions