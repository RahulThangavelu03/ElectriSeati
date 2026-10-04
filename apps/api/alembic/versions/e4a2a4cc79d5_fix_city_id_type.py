"""fix city id type

Revision ID: e4a2a4cc79d5
Revises: 22bfc8cf0ae1
Create Date: 2026-10-02 20:42:20.378698

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e4a2a4cc79d5'
down_revision: Union[str, Sequence[str], None] = '22bfc8cf0ae1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade() -> None:
    op.alter_column(
        "cities",
        "id",
        existing_type=sa.String(),
        type_=sa.Integer(),
        existing_nullable=False,
        postgresql_using="id::integer",
    )


def downgrade() -> None:
    op.alter_column(
        "cities",
        "id",
        existing_type=sa.Integer(),
        type_=sa.String(),
        existing_nullable=False,
        postgresql_using="id::varchar",
    )