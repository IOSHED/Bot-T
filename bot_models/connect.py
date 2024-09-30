from abc import ABC, abstractmethod
from typing import Self
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Session:
    """
    Объект, хранящий в себе любую `session` из разных db.
    Реализует паттерн UnitOfWork.
    """
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def commit(self):
        try:
            await self.session.commit()
        except Exception as e:
            await self.session.rollback()
            raise e

    async def rollback(self):
        await self.session.rollback()

    async def close(self):
        await self.session.close()


class Connect(ABC):
    @abstractmethod
    async def get_session(self) -> Session:
        """Генерирует `session`"""
        ...

    @abstractmethod
    async def create_connect(self, path: str) -> Self:
        """
        Подключается к db
        :param path путь, по которому подключается db
        """
        ...


class PostgresConnect(Connect):
    def __init__(self):
        self._engine = None
        self._sessionmaker = None

    async def create_connect(self, path: str) -> Self:
        """
        Подключается к PostgreSQL по указанному пути.
        """
        self._engine = create_async_engine(path, echo=True, future=True)
        self._sessionmaker = async_sessionmaker(
            bind=self._engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autoflush=False,
        )
        return self

    async def get_session(self) -> Session:
        """
        Создает и возвращает объект `Session` для работы с БД.
        """
        async with self._sessionmaker() as session:
            return Session(session)
