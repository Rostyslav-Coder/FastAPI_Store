"""src/domain/orders/repository.py"""

from typing import Any, AsyncGenerator

from sqlalchemy import Result, select

from src.domain.constants import OrderStatus
from src.domain.orders.models import Order, OrderUncommited
from src.infrastructure.database import BaseRepository, OrdersTable
from src.infrastructure.database.tables import ConcreteTable

__all__ = ("OrdersRepository",)


class OrdersRepository(BaseRepository[OrdersTable]):
    schema_class = OrdersTable

    async def all(
        self, skip_: int = 0, limit_: int | None = None
    ) -> AsyncGenerator[Order, None]:
        async for instance in self._all(skip=skip_, limit=limit_):
            yield Order.from_orm(instance)

    async def all_pending(
        self, value_: int, skip_: int = 0, limit_: int | None = None
    ) -> AsyncGenerator[ConcreteTable, None]:
        query = (
            select(self.schema_class)
            .where(self.schema_class.user_id == value_)
            .where(self.schema_class.status == OrderStatus.PENDING)
            .offset(skip_)
        )

        if limit_ is not None:
            query = query.limit(limit_)

        result: Result = await self.execute(query)

        schemas = result.scalars().all()

        for schema in schemas:
            yield schema

    async def all_paid(
        self, value_: int | None, skip_: int = 0, limit_: int | None = None
    ) -> AsyncGenerator[ConcreteTable, None]:
        query = select(self.schema_class).where(
            self.schema_class.status == OrderStatus.PAID
        )

        if value_ is not None:
            query = query.where(self.schema_class.user_id == value_)

        query = query.offset(skip_)

        if limit_ is not None:
            query = query.limit(limit_)

        result: Result = await self.execute(query)

        schemas = result.scalars().all()

        for schema in schemas:
            yield schema

    async def get(self, key_: str, value_: Any) -> Order:
        instance = await self._get(key=key_, value=value_)
        return Order.from_orm(instance)

    async def create(self, schema: OrderUncommited) -> Order:
        instance: OrdersTable = await self._save(schema.dict())
        return Order.from_orm(instance)

    async def update(
        self, key_: str, value_: Any, payload_: dict[str, Any]
    ) -> Order:
        instance = await self._update(key=key_, value=value_, payload=payload_)
        return Order.from_orm(instance)

    async def delete(self, id_: int) -> None:
        await self._delete(id_)
