"""add phone_number column

Revision ID: bc89e4808ac6
Revises: bfbf44a6f371
Create Date: 2025-08-14 22:13:05.059904

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bc89e4808ac6'
down_revision: Union[str, Sequence[str], None] = 'bfbf44a6f371'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('users',sa.Column('phone_number',sa.String(),nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('users','phone_number')
    pass
