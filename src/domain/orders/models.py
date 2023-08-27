"""src/domain/orders/models.py"""

from datetime import datetime

from pydantic import Field

from src.domain.constants import OrderStatus
from src.infrastructure.models import InternalModel, PublicModel

__all__ = (
    "OrderCreateRequestBody",
    "OrderPublic",
    "OrderUncommited",
    "Order",
)


# Public models
# ------------------------------------------------------
class _OrderPublic(PublicModel):
    """Base class for public order schemas. Defines common fields
    that are present in all public order schemas.
    """

    product_id: int = Field(description="OpenAPI description")
    amount: int = Field(description="OpenAPI description")


class OrderCreateRequestBody(_OrderPublic):
    """Order create request body."""

    pass


class OrderPublic(_OrderPublic):
    """The internal application representation."""

    id: int
    user_id: int
    delivery_address: str
    status: OrderStatus
    order_date: datetime


# Internal models
# ------------------------------------------------------
class _OrderInternal(InternalModel):
    """Base class for internal order schemas. Defines common fields
    that are present in all internal order schemas.
    """

    product_id: int
    amount: int
    user_id: int
    delivery_address: str
    status: OrderStatus = OrderStatus.PENDING
    order_date: datetime


class OrderUncommited(_OrderInternal):
    """This schema is used for creating instance in the database."""

    pass


class Order(_OrderInternal):
    """Existed order representation."""

    id: int
