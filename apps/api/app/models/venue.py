from sqlalchemy import ForeignKey, String, Index, func
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Venue(Base):

    __tablename__ = "venues"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

    location: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

    city_id: Mapped[int | None] = mapped_column(
        ForeignKey("cities.id"),
        nullable=True
    )


Index(
    "uq_venue_name_location",
    func.lower(Venue.name),
    func.lower(Venue.location),
    unique=True
)