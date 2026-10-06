from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from database import Base



class Inventory(Base):

    __tablename__="inventories"

    id:Mapped[int]=mapped_column(primary_key=True)

    event_id:Mapped[int]=mapped_column(ForeignKey("events.id"),nullable=False)

    total_capacity:Mapped[int] =mapped_column(nullable=False)

    locked_quantity:Mapped[int]=mapped_column(nullable=False)

    sold_quantity:Mapped[int]=mapped_column(nullable=False)


