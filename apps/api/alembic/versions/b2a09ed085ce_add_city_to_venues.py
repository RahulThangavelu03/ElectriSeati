"""add city to venues

Revision ID: b2a09ed085ce
Revises: e4a2a4cc79d5
Create Date: 2026-10-04 10:48:25.468049

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b2a09ed085ce'
down_revision: Union[str, Sequence[str], None] = 'e4a2a4cc79d5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None




def upgrade() -> None:
    op.add_column(
        "venues",
        sa.Column("city_id", sa.Integer(), nullable=True)
    )

    op.create_foreign_key(
        "fk_venues_city_id",
        "venues",
        "cities",
        ["city_id"],
        ["id"]
    )
    
def downgrade() -> None:
    op.drop_constraint(
        "fk_venues_city_id",
        "venues",
        type_="foreignkey"
    )

    op.drop_column(
        "venues",
        "city_id"
    )