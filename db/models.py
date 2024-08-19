from sqlalchemy import BigInteger, ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine


# Инициализация движка
engine = create_async_engine(
    url='sqlite+aiosqlite:///db/db.sqlite3',
    echo=True
)

# Сессия для подключения
async_session = async_sessionmaker(engine)


class Base(DeclarativeBase):
    pass


# Сущность пользователя
class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger, unique=True)
    name: Mapped[str] = mapped_column(String(32))


# Сущность документа
class Doc(Base):
    __tablename__ = 'docs'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
