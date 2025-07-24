"""Category endpoints."""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Request, status

from app.dependencies import CurrentUser, DatabaseSession
from app.schemas.base import PaginationParams
from app.schemas.category import (
    CategoryCreate,
    CategoryListResponse,
    CategoryResponse,
    CategoryUpdate,
)
from app.services.category import CategoryService

router = APIRouter()


@router.post(
    "/",
    response_model=CategoryResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new category",
    description="Create a new category for the authenticated user",
)
async def create_category(
    request: Request,
    category: CategoryCreate,
    current_user: CurrentUser,
    db: DatabaseSession,
) -> CategoryResponse:
    """Create a new category."""
    service = CategoryService(db)

    try:
        created_category = await service.create_category(
            user_id=UUID(current_user), category_data=category
        )
        return CategoryResponse.model_validate(created_category)
    except ValueError as e:
        # Make error messages more user-friendly
        error_msg = str(e)
        if "already exists" in error_msg.lower():
            detail = f"A category with the name '{category.name}' already exists"
        else:
            detail = error_msg
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=detail) from e


@router.get(
    "/",
    response_model=CategoryListResponse,
    summary="Get all categories",
    description=(
        "Get all categories for the authenticated user with pagination and search"
    ),
)
async def get_categories(
    request: Request,
    current_user: CurrentUser,
    db: DatabaseSession,
    pagination: Annotated[PaginationParams, Depends()],
    search: str | None = None,
    sort_by: str = "created_at",
    order: str = "desc",
) -> CategoryListResponse:
    """Get all categories with pagination and filtering."""
    service = CategoryService(db)
    categories, total = await service.get_categories(
        user_id=UUID(current_user),
        limit=pagination.limit,
        offset=pagination.offset,
        search=search,
        sort_by=sort_by,
        order=order,
    )

    return CategoryListResponse(
        items=[CategoryResponse.model_validate(category) for category in categories],
        total=total,
        limit=pagination.limit,
        offset=pagination.offset,
    )


@router.get(
    "/{category_id}",
    response_model=CategoryResponse,
    summary="Get a specific category",
    description="Get a specific category by ID",
)
async def get_category(
    request: Request,
    category_id: UUID,
    current_user: CurrentUser,
    db: DatabaseSession,
) -> CategoryResponse:
    """Get a specific category."""
    service = CategoryService(db)
    category = await service.get_category(
        category_id=category_id, user_id=UUID(current_user)
    )

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=(
                f"Category with ID {category_id} not found or "
                "you don't have access to it"
            ),
        )

    return CategoryResponse.model_validate(category)


@router.patch(
    "/{category_id}",
    response_model=CategoryResponse,
    summary="Update a category",
    description="Update a specific category (partial update)",
)
async def update_category(
    request: Request,
    category_id: UUID,
    category_update: CategoryUpdate,
    current_user: CurrentUser,
    db: DatabaseSession,
) -> CategoryResponse:
    """Update a category."""
    service = CategoryService(db)

    try:
        updated_category = await service.update_category(
            category_id=category_id,
            user_id=UUID(current_user),
            category_data=category_update,
        )

        if not updated_category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=(
                    f"Category with ID {category_id} not found or "
                    "you don't have access to it"
                ),
            )

        return CategoryResponse.model_validate(updated_category)
    except ValueError as e:
        # Make error messages more user-friendly
        error_msg = str(e)
        if "already exists" in error_msg.lower():
            detail = f"A category with the name '{category_update.name}' already exists"
        else:
            detail = error_msg
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=detail) from e


@router.delete(
    "/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a category",
    description="Delete a specific category",
)
async def delete_category(
    request: Request,
    category_id: UUID,
    current_user: CurrentUser,
    db: DatabaseSession,
) -> None:
    """Delete a category."""
    service = CategoryService(db)
    deleted = await service.delete_category(
        category_id=category_id, user_id=UUID(current_user)
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=(
                f"Category with ID {category_id} not found or "
                "you don't have access to it"
            ),
        )
