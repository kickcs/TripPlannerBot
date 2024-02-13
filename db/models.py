from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import BigInteger
from typing import Annotated, Optional
from db.database import Base
import enum

int_pk = Annotated[int, mapped_column(BigInteger, primary_key=True)]

class Language(enum.Enum):
    RU = "ru"
    EN = "en"
    UZ = "uz"

class User(Base):
    __tablename__ = "users"

    id: Mapped[int_pk]
    tg_id: Mapped[int] = mapped_column(unique=True)
    language: Mapped[Language] = mapped_column(default=Language.RU)


class Place(Base):
    __tablename__ = "places"

    id: Mapped[int_pk]
    category: Mapped[str]
    subcategory: Mapped[str]
    name: Mapped[str] = mapped_column()
    description: Mapped[str]
    address: Mapped[Optional[str]]
    image_id: Mapped[Optional[str]]

