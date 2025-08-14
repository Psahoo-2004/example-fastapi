"""create table posts

Revision ID: 654e071a251d
Revises: 
Create Date: 2025-08-14 20:49:26.047984

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '654e071a251d'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('posts',sa.Column('id',sa.Integer(),nullable=False,primary_key=True),
                            sa.Column('title',sa.String(),nullable=False)
    )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop('table')
    pass