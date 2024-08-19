from sqlalchemy import select
from db.models import async_session
from db.models import User


# Добавление пользователя в БД
async def set_user(tg_id: int, name: str) -> None:
    async with async_session() as session:
        async with session.begin():
            # Проверка на наличие пользователя в БД
            user = await session.scalar(
                select(User).where(User.tg_id == tg_id)
            )
            # Если пользователя нет, то добавляем его
            if not user:
                session.add(User(tg_id=tg_id, name=name))
                await session.commit()
