"""src/domain/users/repository.py"""

from typing import Any, AsyncGenerator

from src.domain.users.models import User, UserUncommited
from src.infrastructure.database import BaseRepository, UsersTable

__all__ = ("UsersRepository",)


class UsersRepository(BaseRepository[UsersTable]):
    schema_class = UsersTable

    async def all(
        self, skip_: int = 0, limit_: int | None = None
    ) -> AsyncGenerator[User, None]:
        async for instance in self._all(skip=skip_, limit=limit_):
            yield User.from_orm(instance)

    async def get(self, key_: str, value_: Any) -> User:
        instance = await self._get(key=key_, value=value_)
        return User.from_orm(instance)

    async def create(self, schema: UserUncommited) -> User:
        instance: UsersTable = await self._save(schema.dict())
        return User.from_orm(instance)

    async def update(
        self, key_: str, value_: Any, payload_: UserUncommited
    ) -> User:
        instance: UsersTable = await self._update(
            key=key_, value=value_, payload=payload_.dict()
        )
        return User.from_orm(instance)
