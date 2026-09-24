from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Index
from database import Base

from sqlalchemy import Index, func


class Venue(Base):

    __tablename__ = "venues"

  

 
    __table_args__ = (
    Index(
        "uq_venue_name_location",
        "name",
        "location",
        unique=True
    ),
)
    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

    location: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )


Index(
    "uq_venue_name_location",
    func.lower(Venue.name),
    func.lower(Venue.location),
    unique=True
)