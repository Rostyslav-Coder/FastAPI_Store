"""src/infrastructure/database/tables.py"""

from datetime import datetime
from typing import TypeVar

from sqlalchemy import (
    Boolean,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    MetaData,
    String,
)
from sqlalchemy.orm import (
    Mapped,
    declarative_base,
    mapped_column,
    relationship,
)

from src.domain.constants import OrderStatus

__all__ = ("UsersTable", "ProductsTable", "OrdersTable")

meta = MetaData(
    naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_`%(constraint_name)s`",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }
)


class _Base:
    """Base class for all database models."""

    id: Mapped[int] = mapped_column(Integer, primary_key=True)


Base = declarative_base(cls=_Base, metadata=meta)

ConcreteTable = TypeVar("ConcreteTable", bound=Base)


class UsersTable(Base):
    """Class creates a user table in the database"""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(length=320), nullable=False)
    phone_number: Mapped[str] = mapped_column(
        String(length=16), nullable=False
    )
    password: Mapped[str] = mapped_column(String(length=1024), nullable=False)
    first_name: Mapped[str] = mapped_column(String(length=100), nullable=True)
    last_name: Mapped[str] = mapped_column(String(length=100), nullable=True)
    address: Mapped[str] = mapped_column(String(length=1024), nullable=False)
    is_manager: Mapped[bool] = mapped_column(Boolean, default=False)

    orders = relationship("OrdersTable", back_populates="user")


class ProductsTable(Base):
    """Class creates a product table in the database"""

    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(
        String(length=100), unique=True, nullable=False
    )
    title: Mapped[str] = mapped_column(String(length=1024), nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    amount: Mapped[int] = mapped_column(Integer, nullable=False)

    order = relationship("OrdersTable", back_populates="product")


class OrdersTable(Base):
    """Class creates a product table in the database"""

    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    product_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(ProductsTable.id),
        nullable=False,
    )
    amount: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(UsersTable.id),
        nullable=False,
    )
    delivery_address: Mapped[str] = mapped_column(
        String(length=1024), nullable=True
    )
    status: Mapped[Enum] = mapped_column(
        Enum(OrderStatus), nullable=False, default=OrderStatus.PENDING
    )
    order_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    user = relationship("UsersTable", back_populates="orders")
    product = relationship("ProductsTable", back_populates="order")
