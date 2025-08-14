"""add content column to posts table

Revision ID: 0b0037c9365b
Revises: 654e071a251d
Create Date: 2025-08-14 20:51:41.306229

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0b0037c9365b'
down_revision: Union[str, Sequence[str], None] = '654e071a251d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts','content')
    pass
