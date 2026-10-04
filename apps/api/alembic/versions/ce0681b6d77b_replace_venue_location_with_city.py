"""replace venue location with city

Revision ID: ce0681b6d77b
Revises: b2a09ed085ce
Create Date: 2026-10-04 11:39:57.047321

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ce0681b6d77b'
down_revision: Union[str, Sequence[str], None] = 'b2a09ed085ce'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.drop_index(
        "uq_venue_name_location",
        table_name="venues"
    )

    op.drop_column(
        "venues",
        "location"
    )

    op.alter_column(
        "venues",
        "city_id",
        existing_type=sa.Integer(),
        nullable=False
    )

    op.create_index(
        "uq_venue_name_city",
        "venues",
        [
            sa.literal_column("lower(name)"),
            "city_id"
        ],
        unique=True
    )


def downgrade() -> None:
    op.drop_index(
        "uq_venue_name_city",
        table_name="venues"
    )

    op.add_column(
        "venues",
        sa.Column(
            "location",
            sa.String(length=200),
            nullable=True
        )
    )

    op.alter_column(
        "venues",
        "city_id",
        existing_type=sa.Integer(),
        nullable=True
    )

    op.create_index(
        "uq_venue_name_location",
        "venues",
        ["name", "location"],
        unique=True
    )
