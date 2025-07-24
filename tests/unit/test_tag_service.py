"""Unit tests for tag service."""

from uuid import uuid4

import pytest

from app.schemas.tag import TagCreate, TagUpdate
from app.services.tag import TagService


@pytest.mark.asyncio
async def test_create_tag(async_session):
    """Test creating a new tag."""
    service = TagService(async_session)
    tag_data = TagCreate(name="urgent", color="#FF0000")

    tag = await service.create(tag_data)

    assert tag.id is not None
    assert tag.name == "urgent"
    assert tag.color == "#FF0000"
    assert tag.created_at is not None
    assert tag.updated_at is not None


@pytest.mark.asyncio
async def test_create_tag_duplicate_name(async_session):
    """Test creating a tag with duplicate name raises error."""
    service = TagService(async_session)

    # Create first tag
    tag_data = TagCreate(name="urgent")
    await service.create(tag_data)

    # Try to create duplicate
    with pytest.raises(ValueError, match="already exists"):
        await service.create(tag_data)


@pytest.mark.asyncio
async def test_get_tag_by_id(async_session):
    """Test getting a tag by ID."""
    service = TagService(async_session)

    # Create tag
    tag_data = TagCreate(name="work")
    created_tag = await service.create(tag_data)

    # Get by ID
    tag = await service.get_by_id(created_tag.id)

    assert tag is not None
    assert tag.id == created_tag.id
    assert tag.name == "work"


@pytest.mark.asyncio
async def test_get_tag_by_id_not_found(async_session):
    """Test getting a non-existent tag returns None."""
    service = TagService(async_session)

    tag = await service.get_by_id(uuid4())

    assert tag is None


@pytest.mark.asyncio
async def test_get_tag_by_name(async_session):
    """Test getting a tag by name."""
    service = TagService(async_session)

    # Create tag
    tag_data = TagCreate(name="important")
    await service.create(tag_data)

    # Get by name
    tag = await service.get_by_name("important")

    assert tag is not None
    assert tag.name == "important"


@pytest.mark.asyncio
async def test_get_all_tags(async_session):
    """Test getting all tags."""
    service = TagService(async_session)

    # Create multiple tags
    tags_data = [
        TagCreate(name="urgent"),
        TagCreate(name="work"),
        TagCreate(name="personal"),
    ]

    for tag_data in tags_data:
        await service.create(tag_data)

    # Get all
    tags = await service.get_all()

    assert len(tags) == 3
    # Should be ordered by name
    assert tags[0].name == "personal"
    assert tags[1].name == "urgent"
    assert tags[2].name == "work"


@pytest.mark.asyncio
async def test_update_tag(async_session):
    """Test updating a tag."""
    service = TagService(async_session)

    # Create tag
    tag_data = TagCreate(name="urgent", color="#FF0000")
    created_tag = await service.create(tag_data)

    # Update
    update_data = TagUpdate(name="very urgent", color="#FF5500")
    updated_tag = await service.update(created_tag.id, update_data)

    assert updated_tag is not None
    assert updated_tag.name == "very urgent"
    assert updated_tag.color == "#FF5500"


@pytest.mark.asyncio
async def test_update_tag_duplicate_name(async_session):
    """Test updating a tag with duplicate name raises error."""
    service = TagService(async_session)

    # Create two tags
    await service.create(TagCreate(name="urgent"))
    tag2 = await service.create(TagCreate(name="work"))

    # Try to update tag2 with tag1's name
    update_data = TagUpdate(name="urgent")

    with pytest.raises(ValueError, match="already exists"):
        await service.update(tag2.id, update_data)


@pytest.mark.asyncio
async def test_update_tag_not_found(async_session):
    """Test updating a non-existent tag returns None."""
    service = TagService(async_session)

    update_data = TagUpdate(name="new name")
    tag = await service.update(uuid4(), update_data)

    assert tag is None


@pytest.mark.asyncio
async def test_delete_tag(async_session):
    """Test deleting a tag."""
    service = TagService(async_session)

    # Create tag
    tag_data = TagCreate(name="temporary")
    created_tag = await service.create(tag_data)

    # Delete
    deleted = await service.delete(created_tag.id)
    assert deleted is True

    # Verify it's gone
    tag = await service.get_by_id(created_tag.id)
    assert tag is None


@pytest.mark.asyncio
async def test_delete_tag_not_found(async_session):
    """Test deleting a non-existent tag returns False."""
    service = TagService(async_session)

    deleted = await service.delete(uuid4())

    assert deleted is False


@pytest.mark.asyncio
async def test_get_by_ids(async_session):
    """Test getting multiple tags by IDs."""
    service = TagService(async_session)

    # Create tags
    tag1 = await service.create(TagCreate(name="tag1"))
    tag2 = await service.create(TagCreate(name="tag2"))
    tag3 = await service.create(TagCreate(name="tag3"))

    # Get by IDs
    tags = await service.get_by_ids([tag1.id, tag3.id])

    assert len(tags) == 2
    tag_names = {tag.name for tag in tags}
    assert tag_names == {"tag1", "tag3"}


@pytest.mark.asyncio
async def test_get_by_ids_empty_list(async_session):
    """Test getting tags with empty ID list."""
    service = TagService(async_session)

    tags = await service.get_by_ids([])

    assert tags == []
