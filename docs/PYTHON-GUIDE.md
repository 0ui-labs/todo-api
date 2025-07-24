# Python Development Guide

Comprehensive guidance for Python development in this repository.

## Table of Contents

- [Core Philosophy](#core-philosophy)
- [Code Structure](#code-structure)
- [Development Environment](#development-environment)
- [Style & Conventions](#style--conventions)
- [Testing Strategy](#testing-strategy)
- [Error Handling](#error-handling)
- [Data Models](#data-models)
- [Database Standards](#database-standards)
- [Git Workflow](#git-workflow)
- [Performance & Security](#performance--security)
- [Debugging & Monitoring](#debugging--monitoring)

## Core Philosophy

### KISS (Keep It Simple, Stupid)
Choose straightforward solutions over complex ones. Simple solutions are easier to understand, maintain, and debug.

### YAGNI (You Aren't Gonna Need It)
Implement features only when needed, not when you anticipate they might be useful.

### Design Principles
- **Dependency Inversion**: High-level modules should not depend on low-level modules
- **Open/Closed Principle**: Open for extension, closed for modification
- **Single Responsibility**: Each unit should have one clear purpose
- **Fail Fast**: Check for errors early and raise exceptions immediately

## Code Structure

### File and Function Limits
- **Files**: Never exceed 500 lines
- **Functions**: Under 50 lines with single responsibility
- **Classes**: Under 100 lines representing single concept
- **Line length**: Max 100 characters (ruff rule)

### Project Architecture

```
src/project/
    __init__.py
    main.py
    tests/
        test_main.py
    conftest.py
    
    # Core modules
    database/
        __init__.py
        connection.py
        models.py
        tests/
            test_connection.py
            test_models.py
    
    # Feature slices
    features/
        user_management/
            __init__.py
            handlers.py
            validators.py
            tests/
                test_handlers.py
                test_validators.py
```

## Development Environment

### UV Package Management

```bash
# Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment
uv venv

# Sync dependencies
uv sync

# Add packages (NEVER edit pyproject.toml directly!)
uv add requests
uv add --dev pytest ruff mypy

# Run commands
uv run python script.py
uv run pytest
uv run ruff check .
```

### Development Commands

```bash
# Testing
uv run pytest                          # All tests
uv run pytest tests/test_module.py -v  # Specific tests
uv run pytest --cov=src --cov-report=html  # With coverage

# Code Quality
uv run ruff format .                   # Format code
uv run ruff check .                    # Check linting
uv run ruff check --fix .              # Auto-fix issues
uv run mypy src/                       # Type checking
```

## Style & Conventions

### Python Style Guide
- Follow PEP8 with these specifics:
  - Line length: 100 characters
  - Use double quotes for strings
  - Use trailing commas in multi-line structures
- Always use type hints
- Format with `ruff format`
- Use Pydantic v2 for validation

### Docstring Standards

```python
def calculate_discount(
    price: Decimal,
    discount_percent: float,
    min_amount: Decimal = Decimal("0.01")
) -> Decimal:
    """
    Calculate the discounted price for a product.
    
    Args:
        price: Original price of the product
        discount_percent: Discount percentage (0-100)
        min_amount: Minimum allowed final price
        
    Returns:
        Final price after applying discount
        
    Raises:
        ValueError: If discount_percent is not between 0 and 100
        ValueError: If final price would be below min_amount
        
    Example:
        >>> calculate_discount(Decimal("100"), 20)
        Decimal('80.00')
    """
```

### Naming Conventions
- **Variables/functions**: `snake_case`
- **Classes**: `PascalCase`
- **Constants**: `UPPER_SNAKE_CASE`
- **Private**: `_leading_underscore`
- **Type aliases**: `PascalCase`
- **Enum values**: `UPPER_SNAKE_CASE`

## Testing Strategy

### Test-Driven Development (TDD)
1. Write the test first
2. Watch it fail
3. Write minimal code to pass
4. Refactor
5. Repeat

### Testing Best Practices

```python
import pytest
from datetime import datetime

@pytest.fixture
def sample_user():
    """Provide a sample user for testing."""
    return User(
        id=123,
        name="Test User",
        email="test@example.com",
        created_at=datetime.now()
    )

def test_user_can_update_email_when_valid(sample_user):
    """Test that users can update their email with valid input."""
    new_email = "newemail@example.com"
    sample_user.update_email(new_email)
    assert sample_user.email == new_email

def test_user_update_email_fails_with_invalid_format(sample_user):
    """Test that invalid email formats are rejected."""
    with pytest.raises(ValidationError) as exc_info:
        sample_user.update_email("not-an-email")
    assert "Invalid email format" in str(exc_info.value)
```

### Test Organization
- **Unit tests**: Test individual functions/methods
- **Integration tests**: Test component interactions
- **End-to-end tests**: Test complete workflows
- Keep tests next to code
- Use `conftest.py` for shared fixtures
- Aim for 80%+ coverage on critical paths

## Error Handling

### Exception Best Practices

```python
# Custom domain exceptions
class PaymentError(Exception):
    """Base exception for payment-related errors."""
    pass

class InsufficientFundsError(PaymentError):
    """Raised when account has insufficient funds."""
    def __init__(self, required: Decimal, available: Decimal):
        self.required = required
        self.available = available
        super().__init__(
            f"Insufficient funds: required {required}, available {available}"
        )

# Specific exception handling
try:
    process_payment(amount)
except InsufficientFundsError as e:
    logger.warning(f"Payment failed: {e}")
    return PaymentResult(success=False, reason="insufficient_funds")
except PaymentError as e:
    logger.error(f"Payment error: {e}")
    return PaymentResult(success=False, reason="payment_error")
```

### Context Managers

```python
from contextlib import contextmanager

@contextmanager
def database_transaction():
    """Provide a transactional scope for database operations."""
    conn = get_connection()
    trans = conn.begin_transaction()
    try:
        yield conn
        trans.commit()
    except Exception:
        trans.rollback()
        raise
    finally:
        conn.close()
```

## Data Models

### Pydantic Models (v2)

```python
from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional, List
from decimal import Decimal

class ProductBase(BaseModel):
    """Base product model with common fields."""
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    price: Decimal = Field(..., gt=0, decimal_places=2)
    category: str
    tags: List[str] = []
    
    @validator('price')
    def validate_price(cls, v):
        if v > Decimal('1000000'):
            raise ValueError('Price cannot exceed 1,000,000')
        return v
    
    class Config:
        json_encoders = {
            Decimal: str,
            datetime: lambda v: v.isoformat()
        }

class Product(ProductBase):
    """Complete product model with database fields."""
    id: int
    created_at: datetime
    updated_at: datetime
    is_active: bool = True
    
    class Config:
        from_attributes = True  # Enable ORM mode
```

### Settings Management

```python
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    """Application settings with validation."""
    app_name: str = "MyApp"
    debug: bool = False
    database_url: str
    redis_url: str = "redis://localhost:6379"
    api_key: str
    max_connections: int = 100
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
```

## Database Standards

### Entity-Specific Primary Keys

```sql
-- ✅ STANDARDIZED: Entity-specific primary keys
sessions.session_id UUID PRIMARY KEY
leads.lead_id UUID PRIMARY KEY
messages.message_id UUID PRIMARY KEY
```

### Field Naming Conventions

```sql
-- Primary keys: {entity}_id
session_id, lead_id, message_id

-- Foreign keys: {referenced_entity}_id
session_id REFERENCES sessions(session_id)

-- Timestamps: {action}_at
created_at, updated_at, started_at, expires_at

-- Booleans: is_{state}
is_connected, is_active, is_qualified

-- Counts: {entity}_count
message_count, lead_count, notification_count
```

### Repository Pattern

```python
# Convention-based repositories
class LeadRepository(BaseRepository[Lead]):
    def __init__(self):
        super().__init__()  # Auto-derives "leads" and "lead_id"
```

## Git Workflow

### Branch Strategy
- `main` - Production-ready code
- `develop` - Integration branch
- `feature/*` - New features
- `fix/*` - Bug fixes
- `docs/*` - Documentation
- `refactor/*` - Code refactoring
- `test/*` - Test additions

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

Types: feat, fix, docs, style, refactor, test, chore

Example:
```
feat(auth): add two-factor authentication

- Implement TOTP generation and validation
- Add QR code generation for authenticator apps
- Update user model with 2FA fields

Closes #123
```

## Performance & Security

### Performance Guidelines
- Profile before optimizing
- Use `lru_cache` for expensive computations
- Prefer generators for large datasets
- Use `asyncio` for I/O-bound operations
- Consider `multiprocessing` for CPU-bound tasks

### Security Best Practices
- Never commit secrets
- Validate all user input
- Use parameterized queries
- Implement rate limiting
- Keep dependencies updated
- Use HTTPS for external communications
- Proper authentication/authorization

### Example Security Implementation

```python
from passlib.context import CryptContext
import secrets

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash password using bcrypt."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)

def generate_secure_token(length: int = 32) -> str:
    """Generate a cryptographically secure random token."""
    return secrets.token_urlsafe(length)
```

## Debugging & Monitoring

### Debugging Tools

```bash
# Interactive debugging
uv add --dev ipdb
# Add breakpoint: import ipdb; ipdb.set_trace()

# Memory profiling
uv add --dev memory-profiler
uv run python -m memory_profiler script.py

# Rich traceback
uv add --dev rich
# In code: from rich.traceback import install; install()
```

### Structured Logging

```python
import structlog

logger = structlog.get_logger()

# Log with context
logger.info(
    "payment_processed",
    user_id=user.id,
    amount=amount,
    currency="USD",
    processing_time=processing_time
)
```

## Search Command Requirements

**CRITICAL**: Always use `rg` (ripgrep) instead of `grep` and `find`:

```bash
# ❌ Don't use grep
grep -r "pattern" .

# ✅ Use rg instead
rg "pattern"

# ❌ Don't use find with name
find . -name "*.py"

# ✅ Use rg with file filtering
rg --files -g "*.py"
```

## Important Notes

- **NEVER ASSUME OR GUESS** - Ask for clarification when unsure
- **Always verify file paths and module names**
- **Keep documentation updated**
- **Test your code** - No feature is complete without tests
- **Document your decisions**

---

_This is a living guide. Update it as the project evolves and new patterns emerge._