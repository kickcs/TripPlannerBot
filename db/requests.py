from sqlalchemy import select, delete, join, func
from db.database import async_session_factory
from db.models import User, Place, Bookmark

from typing import Optional


class UserORM:

    @staticmethod
    async def create_user(user_id: int):
        async with async_session_factory() as session:
            session.add(User(tg_id=user_id))
            await session.commit()

    @staticmethod
    async def get_user(user_id: int):
        async with async_session_factory() as session:
            user = await session.execute(select(User).where(User.tg_id == user_id))
            return user.scalars().first()


class PlaceORM:

    @staticmethod
    async def create_place(category: str, subcategory: str, name: str, desc: str, address: Optional[str],
                           image_id: Optional[str]):
        async with async_session_factory() as session:
            session.add(Place(category=category,
                              subcategory=subcategory,
                              name=name,
                              description=desc,
                              address=None if address is None else address,
                              image_id=image_id))
            await session.commit()

    @staticmethod
    async def delete_place(place_id: int):
        async with async_session_factory() as session:
            await session.execute(delete(Bookmark).where(Bookmark.place_id == place_id))
            await session.execute(delete(Place).where(Place.id == place_id))
            await session.commit()

    @staticmethod
    async def get_place(place_id: int):
        async with async_session_factory() as session:
            place = await session.execute(select(Place).where(Place.id == place_id))
            return place.scalars().first()

    @staticmethod
    async def get_category_places():
        async with async_session_factory() as session:
            result = await session.execute(select(Place.category).distinct())
            return result.scalars().unique().all()

    @staticmethod
    async def get_subcategory_places(category: str):
        async with async_session_factory() as session:
            result = await session.execute(select(Place.subcategory).where(Place.category == category).distinct())
            return result.scalars().unique().all()

    @staticmethod
    async def count_places_by_subcategory(subcategory_name):
        async with async_session_factory() as session:
            result = await session.execute(
                select(func.count(Place.id)).where(Place.subcategory == subcategory_name)
            )
            count = result.scalar()
            return count

    @staticmethod
    async def get_places_with_ordinal_ids(subcategory_name: str):
        async with async_session_factory() as session:
            stmt = select(
                func.row_number().over(
                    partition_by=Place.subcategory,
                    order_by=Place.id
                ).label("ordinal_id"),
                Place.name,
                Place.description,
                Place.image_id
            ).where(Place.subcategory == subcategory_name)
            result = await session.execute(stmt)
            places = result.fetchall()
            return places
