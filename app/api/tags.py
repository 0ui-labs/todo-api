"""Tag API endpoints."""

from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from app.dependencies import CurrentUser, DatabaseSession
from app.middleware.rate_limit import RateLimiters
from app.schemas.tag import TagCreate, TagResponse, TagUpdate
from app.services.tag import TagService

router = APIRouter()


@RateLimiters.tag_create

@router.post("/", response_model=TagResponse, status_code=status.HTTP_201_CREATED)
async def create_tag(
    tag_data: TagCreate,
    db: DatabaseSession,
    current_user_id: CurrentUser,
) -> TagResponse:
    """Create a new tag.

    Args:
        tag_data: Tag creation data
        db: Database session
        current_user: Authenticated user

    Returns:
        Created tag

    Raises:
        HTTPException: If tag name already exists
    """
    service = TagService(db)

    try:
        tag = await service.create(tag_data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    return TagResponse.model_validate(tag)


@RateLimiters.tag_list

@router.get("/", response_model=list[TagResponse])
async def get_tags(
    db: DatabaseSession,
    current_user_id: CurrentUser,
) -> list[TagResponse]:
    """Get all tags.

    Args:
        db: Database session
        current_user: Authenticated user

    Returns:
        List of all tags
    """
    service = TagService(db)
    tags = await service.get_all()
    return [TagResponse.model_validate(tag) for tag in tags]


@RateLimiters.tag_list

@router.get("/{tag_id}", response_model=TagResponse)
async def get_tag(
    tag_id: UUID,
    db: DatabaseSession,
    current_user_id: CurrentUser,
) -> TagResponse:
    """Get a specific tag.

    Args:
        tag_id: Tag ID
        db: Database session
        current_user: Authenticated user

    Returns:
        Tag details

    Raises:
        HTTPException: If tag not found
    """
    service = TagService(db)
    tag = await service.get_by_id(tag_id)

    if not tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tag with id {tag_id} not found"
        )

    return TagResponse.model_validate(tag)


@RateLimiters.tag_update

@router.put("/{tag_id}", response_model=TagResponse)
async def update_tag(
    tag_id: UUID,
    tag_data: TagUpdate,
    db: DatabaseSession,
    current_user_id: CurrentUser,
) -> TagResponse:
    """Update a tag.

    Args:
        tag_id: Tag ID
        tag_data: Update data
        db: Database session
        current_user: Authenticated user

    Returns:
        Updated tag

    Raises:
        HTTPException: If tag not found or name already exists
    """
    service = TagService(db)

    try:
        tag = await service.update(tag_id, tag_data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    if not tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tag with id {tag_id} not found"
        )

    return TagResponse.model_validate(tag)


@RateLimiters.tag_delete

@router.delete("/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tag(
    tag_id: UUID,
    db: DatabaseSession,
    current_user_id: CurrentUser,
) -> None:
    """Delete a tag.

    Args:
        tag_id: Tag ID
        db: Database session
        current_user: Authenticated user

    Raises:
        HTTPException: If tag not found
    """
    service = TagService(db)
    deleted = await service.delete(tag_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tag with id {tag_id} not found"
        )
