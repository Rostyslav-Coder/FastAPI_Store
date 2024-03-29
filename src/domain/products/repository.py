"""src/domain/products/repository.py"""

from typing import Any, AsyncGenerator

from src.domain.products.models import Product, ProductUncommited
from src.infrastructure.database import BaseRepository, ProductsTable

__all__ = ("ProductRepository",)


class ProductRepository(BaseRepository[ProductsTable]):
    schema_class = ProductsTable

    async def all(
        self, skip_: int = 0, limit_: int | None = None
    ) -> AsyncGenerator[Product, None]:
        async for instance in self._all(skip=skip_, limit=limit_):
            yield Product.from_orm(instance)

    async def get(self, key_: str, value_: Any) -> Product:
        instance = await self._get(key=key_, value=value_)
        return Product.from_orm(instance)

    async def create(self, schema_: ProductUncommited) -> Product:
        instance: ProductsTable = await self._save(schema_.dict())
        return Product.from_orm(instance)

    async def update(
        self, key_: str, value_: Any, payload_: dict[str, Any]
    ) -> Product:
        instance = await self._update(key=key_, value=value_, payload=payload_)
        return Product.from_orm(instance)

    async def delete(self, id_: int) -> None:
        await self._delete(id_)
