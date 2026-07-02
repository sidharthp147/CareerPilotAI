"""added columns fro soft delete

Revision ID: 987da3a31564
Revises: 30b7fab0c68e
Create Date: 2026-02-25 16:58:53.551126

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '987da3a31564'
down_revision: Union[str, Sequence[str], None] = '30b7fab0c68e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('jobs', sa.Column('is_deleted', sa.Boolean(), server_default=sa.false()))
    op.add_column('jobs', sa.Column('deleted_at', sa.DateTime(), nullable=True))


def downgrade() -> None:
    
    op.drop_column('jobs', 'is_deleted')
    op.drop_column('jobs', 'deleted_at')
