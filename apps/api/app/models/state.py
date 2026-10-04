from sqlalchemy import ForeignKey ,String
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class State(Base):

    __tablename__="states"


    id:Mapped[int] = mapped_column(primary_key=True)

    name:Mapped[str]=mapped_column(
     String(100),
     nullable=False,

   )

    country_id:Mapped[int]=mapped_column(

     ForeignKey("countries.id"),
     nullable=False,
   )

