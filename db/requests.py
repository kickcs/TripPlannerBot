from sqlalchemy import select, delete, join, func
from db.database import async_session_factory
from db.models import User, Place, Bookmark


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
    pass
