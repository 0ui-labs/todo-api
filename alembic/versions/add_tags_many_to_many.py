"""Add tags table and many-to-many relationship with todos

Revision ID: add_tags_many_to_many
Revises: c5363c8bc7fb
Create Date: 2025-01-23 01:35:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "add_tags_many_to_many"
down_revision: str | None = "c5363c8bc7fb"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # Create tags table
    op.create_table(
        "tags",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.Column("color", sa.String(length=7), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )

    # Create todo_tags association table
    op.create_table(
        "todo_tags",
        sa.Column("todo_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("tag_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["todo_id"], ["todos.id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["tag_id"], ["tags.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("todo_id", "tag_id"),
    )

    # Create indexes for better performance
    op.create_index(op.f("ix_tags_name"), "tags", ["name"], unique=False)
    op.create_index(op.f("ix_todo_tags_todo_id"), "todo_tags", ["todo_id"], unique=False)
    op.create_index(op.f("ix_todo_tags_tag_id"), "todo_tags", ["tag_id"], unique=False)


def downgrade() -> None:
    # Drop indexes
    op.drop_index(op.f("ix_todo_tags_tag_id"), table_name="todo_tags")
    op.drop_index(op.f("ix_todo_tags_todo_id"), table_name="todo_tags")
    op.drop_index(op.f("ix_tags_name"), table_name="tags")

    # Drop tables
    op.drop_table("todo_tags")
    op.drop_table("tags")
