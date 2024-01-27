from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from typing import Annotated
from db.database import Base
from typing import Optional
import enum


int_pk = Annotated[int, mapped_column(primary_key=True)]


class Language(enum.Enum):
    RU = "ru"
    EN = "en"
    UZ = "uz"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int_pk]
    tg_id: Mapped[int] = mapped_column(unique=True)
    language: Mapped[Language] = mapped_column(default=Language.RU)

    bookmarks: Mapped[list["Bookmark"]] = relationship(
        'Bookmark',
        back_populates="user",
    )


class Place(Base):
    __tablename__ = "places"

    id: Mapped[int_pk]
    category: Mapped[str]
    subcategory: Mapped[str]
    name: Mapped[str] = mapped_column()
    description: Mapped[str]
    address: Mapped[Optional[str]]
    image_id: Mapped[Optional[str]]

    bookmarks: Mapped['Bookmark'] = relationship(
        'Bookmark',
        back_populates="place"
    )


class Bookmark(Base):
    __tablename__ = "bookmarks"

    id: Mapped[int_pk]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    place_id: Mapped[int] = mapped_column(ForeignKey("places.id"))

    user: Mapped["User"] = relationship(
        "User", back_populates="bookmarks"
    )
    place: Mapped["Place"] = relationship(
        "Place", back_populates="bookmarks"
    )






