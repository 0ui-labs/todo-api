# Code Style and Conventions

## Python Style
- **Python Version**: 3.11+
- **Type Hints**: Required for all functions/methods (enforced by mypy)
- **Docstrings**: Brief docstrings for all public methods
- **Async/Await**: All database operations and service methods are async
- **Line Length**: 88 characters (Ruff default)

## Naming Conventions
- **Classes**: PascalCase (TodoService, CategoryService)
- **Functions/Methods**: snake_case (create_todo, get_todos)
- **Constants**: UPPER_SNAKE_CASE (TEST_DATABASE_URL)
- **Private Methods**: Leading underscore (_internal_method)

## Type Annotations
```python
async def create_todo(self, user_id: UUID, todo_data: TodoCreate) -> Todo | None:
```

## Error Handling
- Return None for not found cases in service layer
- Let API endpoints handle HTTP status codes
- Use FastAPI's HTTPException for API errors

## Database Models
- All models inherit from Base (SQLAlchemy DeclarativeBase)
- Use UUID for primary keys
- Include created_at, updated_at, deleted_at timestamps
- Relationships defined with back_populates

## Pydantic Schemas
- Separate schemas for Create, Update, and Response
- Use BaseSchema with model_config for JSON serialization
- Field validators for custom validation logic

## Testing
- Unit tests mock dependencies
- Integration tests use test database
- Fixtures in conftest.py for common test data
- Async tests with pytest-asyncio