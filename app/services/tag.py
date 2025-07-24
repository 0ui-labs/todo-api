"""Tag service for business logic."""

from typing import List, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.tag import Tag
from app.schemas.tag import TagCreate, TagUpdate


class TagService:
    """Service class for tag operations."""

    def __init__(self, db: AsyncSession):
        """Initialize tag service.

        Args:
            db: Database session
        """
        self.db = db

    async def create(self, tag_data: TagCreate) -> Tag:
        """Create a new tag.

        Args:
            tag_data: Tag creation data

        Returns:
            Created tag

        Raises:
            ValueError: If tag name already exists
        """
        # Check if tag with same name already exists
        existing_tag = await self.db.execute(
            select(Tag).where(Tag.name == tag_data.name)
        )
        if existing_tag.scalar_one_or_none():
            raise ValueError(f"Tag with name '{tag_data.name}' already exists")

        tag = Tag(**tag_data.model_dump())
        self.db.add(tag)
        
        try:
            await self.db.commit()
            await self.db.refresh(tag)
        except IntegrityError:
            await self.db.rollback()
            raise ValueError(f"Tag with name '{tag_data.name}' already exists")
        
        return tag

    async def get_by_id(self, tag_id: UUID) -> Optional[Tag]:
        """Get tag by ID.

        Args:
            tag_id: Tag ID

        Returns:
            Tag if found, None otherwise
        """
        result = await self.db.execute(
            select(Tag).where(Tag.id == tag_id)
        )
        return result.scalar_one_or_none()

    async def get_by_name(self, name: str) -> Optional[Tag]:
        """Get tag by name.

        Args:
            name: Tag name

        Returns:
            Tag if found, None otherwise
        """
        result = await self.db.execute(
            select(Tag).where(Tag.name == name)
        )
        return result.scalar_one_or_none()

    async def get_all(self) -> List[Tag]:
        """Get all tags.

        Returns:
            List of all tags
        """
        result = await self.db.execute(
            select(Tag).order_by(Tag.name)
        )
        return list(result.scalars().all())

    async def update(self, tag_id: UUID, tag_data: TagUpdate) -> Optional[Tag]:
        """Update a tag.

        Args:
            tag_id: Tag ID
            tag_data: Update data

        Returns:
            Updated tag if found, None otherwise

        Raises:
            ValueError: If new name already exists
        """
        tag = await self.get_by_id(tag_id)
        if not tag:
            return None

        update_data = tag_data.model_dump(exclude_unset=True)
        
        # If updating name, check for duplicates
        if "name" in update_data and update_data["name"] != tag.name:
            existing_tag = await self.get_by_name(update_data["name"])
            if existing_tag:
                raise ValueError(f"Tag with name '{update_data['name']}' already exists")

        for field, value in update_data.items():
            setattr(tag, field, value)

        try:
            await self.db.commit()
            await self.db.refresh(tag)
        except IntegrityError:
            await self.db.rollback()
            raise ValueError("Failed to update tag due to constraint violation")
        
        return tag

    async def delete(self, tag_id: UUID) -> bool:
        """Delete a tag.

        Args:
            tag_id: Tag ID

        Returns:
            True if deleted, False if not found
        """
        tag = await self.get_by_id(tag_id)
        if not tag:
            return False

        await self.db.delete(tag)
        await self.db.commit()
        return True

    async def get_by_ids(self, tag_ids: List[UUID]) -> List[Tag]:
        """Get multiple tags by their IDs.

        Args:
            tag_ids: List of tag IDs

        Returns:
            List of found tags
        """
        if not tag_ids:
            return []

        result = await self.db.execute(
            select(Tag).where(Tag.id.in_(tag_ids))
        )
        return list(result.scalars().all())