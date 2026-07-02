"""add columns in users table fro email verification

Revision ID: 18264f78e7e8
Revises: 987da3a31564
Create Date: 2026-03-17 22:20:11.167767

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '18264f78e7e8'
down_revision: Union[str, Sequence[str], None] = '987da3a31564'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users',sa.Column('is_verfied',sa.Boolean(),nullable=True))
    op.add_column('users',sa.Column('verification_token',sa.String(100),nullable=True))



def downgrade() -> None:
    """Downgrade schema."""
    pass
