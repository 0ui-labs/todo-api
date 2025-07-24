"""Add is_admin field to users table

Revision ID: add_is_admin_001
Revises: add_tags_many_to_many
Create Date: 2025-01-24 09:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'add_is_admin_001'
down_revision: Union[str, None] = 'add_tags_many_to_many'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add is_admin column to users table
    op.add_column('users', sa.Column('is_admin', sa.Boolean(), nullable=False, server_default='false'))


def downgrade() -> None:
    # Remove is_admin column from users table
    op.drop_column('users', 'is_admin')