"""create inventories table

Revision ID: 06091e315359
Revises: ce0681b6d77b
Create Date: 2026-10-05 14:39:07.186911

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '06091e315359'
down_revision: Union[str, Sequence[str], None] = 'ce0681b6d77b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.create_table(
        "inventories",

        sa.Column(
            "id",
            sa.Integer(),
            nullable=False
        ),

        sa.Column(
            "event_id",
            sa.Integer(),
            nullable=False
        ),

        sa.Column(
            "total_capacity",
            sa.Integer(),
            nullable=False
        ),

        sa.Column(
            "sold_quantity",
            sa.Integer(),
            nullable=False
        ),

        sa.Column(
            "locked_quantity",
            sa.Integer(),
            nullable=False
        ),

        sa.ForeignKeyConstraint(
            ["event_id"],
            ["events.id"]
        ),

        sa.PrimaryKeyConstraint("id"),

        sa.UniqueConstraint(
            "event_id",
            name="uq_inventory_event"
        )
    )


def downgrade() -> None:
    op.drop_table("inventories")
