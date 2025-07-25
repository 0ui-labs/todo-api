"""Todo endpoints."""
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Request, status

from app.dependencies import CurrentUser, DatabaseSession
from app.middleware.rate_limit import RateLimiters
from app.models.todo import TodoStatus
from app.schemas.base import PaginationParams
from app.schemas.todo import (
    TodoCreate,
    TodoFilter,
    TodoListResponse,
    TodoResponse,
    TodoSort,
    TodoUpdate,
)
from app.services.todo import TodoService

router = APIRouter()


@RateLimiters.todo_create

@router.post(
    "/",
    response_model=TodoResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new todo",
    description="Create a new todo item for the authenticated user",
)
async def create_todo(
    request: Request,
    todo: TodoCreate,
    current_user: CurrentUser,
    db: DatabaseSession,
) -> TodoResponse:
    """Create a new todo."""
    service = TodoService(db)
    created_todo = await service.create_todo(
        user_id=UUID(current_user),
        todo_data=todo
    )

    # Handle category validation failure
    if not created_todo and todo.category_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )

    return TodoResponse.model_validate(created_todo)


@router.get(
    "/",
    response_model=TodoListResponse,
    summary="Get all todos",
    description=(
        "Get all todos for the authenticated user "
        "with pagination and filtering"
    ),
)
@RateLimiters.todo_list
async def get_todos(
    request: Request,
    current_user: CurrentUser,
    db: DatabaseSession,
    pagination: Annotated[PaginationParams, Depends()],
    status: TodoStatus | None = None,
    category_id: UUID | None = None,
    search: str | None = None,
    sort_by: str = "created_at",
    order: str = "desc",
) -> TodoListResponse:
    """Get all todos with pagination and filtering."""
    # Create filter and sort objects
    filter_params = None
    if status or category_id or search:
        filter_params = TodoFilter(
            status=status,
            category_id=category_id,
            search=search
        )

    sort_params = TodoSort(sort_by=sort_by, order=order)

    service = TodoService(db)
    todos, total = await service.get_todos(
        user_id=UUID(current_user),
        limit=pagination.limit,
        offset=pagination.offset,
        filter_params=filter_params,
        sort_params=sort_params,
    )

    return TodoListResponse(
        items=[TodoResponse.model_validate(todo) for todo in todos],
        total=total,
        limit=pagination.limit,
        offset=pagination.offset,
    )


@router.get(
    "/{todo_id}",
    response_model=TodoResponse,
    summary="Get a specific todo",
    description="Get a specific todo by ID",
)
@RateLimiters.todo_get
async def get_todo(
    request: Request,
    todo_id: UUID,
    current_user: CurrentUser,
    db: DatabaseSession,
) -> TodoResponse:
    """Get a specific todo."""
    service = TodoService(db)
    todo = await service.get_todo(
        todo_id=todo_id,
        user_id=UUID(current_user)
    )

    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )

    return TodoResponse.model_validate(todo)


@router.patch(
    "/{todo_id}",
    response_model=TodoResponse,
    summary="Update a todo",
    description="Update a specific todo (partial update)",
)
@RateLimiters.todo_update
async def update_todo(
    request: Request,
    todo_id: UUID,
    todo_update: TodoUpdate,
    current_user: CurrentUser,
    db: DatabaseSession,
) -> TodoResponse:
    """Update a todo."""
    service = TodoService(db)
    updated_todo = await service.update_todo(
        todo_id=todo_id,
        user_id=UUID(current_user),
        todo_data=todo_update
    )

    if not updated_todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )

    return TodoResponse.model_validate(updated_todo)


@router.put(
    "/{todo_id}",
    response_model=TodoResponse,
    summary="Replace a todo",
    description="Replace a specific todo (full update)",
)
@RateLimiters.todo_update
async def replace_todo(
    request: Request,
    todo_id: UUID,
    todo: TodoCreate,
    current_user: CurrentUser,
    db: DatabaseSession,
) -> TodoResponse:
    """Replace a todo (full update)."""
    # Convert TodoCreate to TodoUpdate with all fields
    todo_update = TodoUpdate(**todo.model_dump())

    service = TodoService(db)
    updated_todo = await service.update_todo(
        todo_id=todo_id,
        user_id=UUID(current_user),
        todo_data=todo_update
    )

    if not updated_todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )

    return TodoResponse.model_validate(updated_todo)


@router.delete(
    "/{todo_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a todo",
    description="Soft delete a specific todo",
)
@RateLimiters.todo_delete
async def delete_todo(
    request: Request,
    todo_id: UUID,
    current_user: CurrentUser,
    db: DatabaseSession,
) -> None:
    """Delete a todo."""
    service = TodoService(db)
    deleted = await service.delete_todo(
        todo_id=todo_id,
        user_id=UUID(current_user)
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
