from sqlalchemy import select

from database import async_session, User


async def set_user(tg_id):
    async with async_session() as session:
        async with session.begin():
            user = await session.scalar(
                select(User).where(User.tg_id == tg_id)
            )

            if not user:
                user = User(tg_id=tg_id)
                await session.commit()
