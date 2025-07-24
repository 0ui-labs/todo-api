"""Tag API endpoints."""

from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_current_user, get_db
from app.models.user import User
from app.schemas.tag import TagCreate, TagResponse, TagUpdate
from app.services.tag import TagService

router = APIRouter()


@router.post("/", response_model=TagResponse, status_code=status.HTTP_201_CREATED)
async def create_tag(
    tag_data: TagCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
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


@router.get("/", response_model=List[TagResponse])
async def get_tags(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> List[TagResponse]:
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


@router.get("/{tag_id}", response_model=TagResponse)
async def get_tag(
    tag_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
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


@router.put("/{tag_id}", response_model=TagResponse)
async def update_tag(
    tag_id: UUID,
    tag_data: TagUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
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


@router.delete("/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tag(
    tag_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
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