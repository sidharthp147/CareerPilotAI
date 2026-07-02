"""add unique key constarint on applications

Revision ID: 30b7fab0c68e
Revises: 
Create Date: 2026-02-23 19:53:53.408801

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '30b7fab0c68e'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint('uq_job_user_application', 'applications', ['job_id', 'job_seeker_id'])


def downgrade() -> None:
    op.drop_constraint('uq_job_user_application', 'applications', type_='unique')