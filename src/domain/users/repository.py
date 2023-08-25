"""src/domain/users/repository.py"""

from typing import AsyncGenerator

from src.domain.users.models import User, UserUncommited
from src.infrastructure.database import BaseRepository, UsersTable

__all__ = ("UsersRepository",)


class UsersRepository(BaseRepository[UsersTable]):
    schema_class = UsersTable

    async def all(self) -> AsyncGenerator[User, None]:
        async for instance in self._all():
            yield User.from_orm(instance)

    async def get(self, id_: int) -> User:
        instance = await self._get(key="id", value=id_)
        return User.from_orm(instance)

    async def get_by_email(self, email_: int) -> User:
        instance = await self._get(key="email", value=email_)
        return User.from_orm(instance)

    async def create(self, schema: UserUncommited) -> User:
        instance: UsersTable = await self._save(schema.dict())
        return User.from_orm(instance)

    async def update(self, id_: int, schema: UserUncommited) -> User:
        instance: UsersTable = await self._update(
            key="id", value=id_, payload=schema.dict()
        )
        return User.from_orm(instance)
