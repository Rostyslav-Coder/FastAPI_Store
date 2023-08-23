"""src/infrastructure/database/session.py"""

from contextvars import ContextVar

from sqlalchemy import Result
from sqlalchemy.exc import IntegrityError, PendingRollbackError
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.config import settings

from ..errors import DatabaseError

__all__ = ("get_session", "engine", "CTX_SESSION")


# Definition of an asynchronous database engine
engine: AsyncEngine = create_async_engine(
    settings.database.url, future=True, pool_pre_ping=True, echo=False
)


def get_session(engine: AsyncEngine | None = engine) -> AsyncSession:
    """Function creates and returns asynchronous database session"""

    Session: async_sessionmaker = async_sessionmaker(
        engine, expire_on_commit=False, autoflush=False
    )

    return Session()


CTX_SESSION: ContextVar[AsyncSession] = ContextVar(
    "session", default=get_session()
)


class Session:
    """Class used to manage database sessions"""

    # All sqlalchemy errors that can be raised
    _ERRORS = (IntegrityError, PendingRollbackError)

    def __init__(self) -> None:
        self._session: AsyncSession = CTX_SESSION.get()

    async def execute(self, query) -> Result:
        try:
            result = await self._session.execute(query)
            return result
        except self._ERRORS:
            raise DatabaseError
