from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.models.event_type import EventType

from database import Base
from app.models.event_type import EventType



class Event(Base):

    __tablename__= "events"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    event_type:Mapped[EventType] = mapped_column(String(50),nullable=False)
    category_id:Mapped[int]=mapped_column(ForeignKey("categories.id"),nullable=False)
    venue: Mapped[str] = mapped_column(String(200),nullable = False)
    starts_at: Mapped[datetime] = mapped_column(DateTime,nullable= False)
    created_at:Mapped[datetime] = mapped_column(
        DateTime,
        default =datetime.utcnow,
        nullable=False,
    )


class CreateEvent(BaseModel):
    title:str
    description:str | None = None
    event_type:EventType
    category_id:int
    venue:str
    starts_at:datetime
