"""src/domain/orders/repository.py"""

from typing import AsyncGenerator

from src.domain.orders.models import Order, OrderUncommited
from src.infrastructure.database import BaseRepository, OrdersTable

__all__ = ("OrdersRepository",)


class OrdersRepository(BaseRepository[OrdersTable]):
    schema_class = OrdersTable

    async def all(self) -> AsyncGenerator[Order, None]:
        async for instance in self._all():
            yield Order.from_orm(instance)

    async def all_my_catr(
        self, user_id: int, skip: int, limit: int
    ) -> AsyncGenerator[Order, None]:
        async for instance in self._all_my_cart(user_id, skip, limit):
            yield Order.from_orm(instance)

    async def get(self, id_: int) -> Order:
        instance = await self._get(key="id", value=id_)
        return Order.from_orm(instance)

    async def create(self, schema: OrderUncommited) -> Order:
        instance: OrdersTable = await self._save(schema.dict())
        return Order.from_orm(instance)
