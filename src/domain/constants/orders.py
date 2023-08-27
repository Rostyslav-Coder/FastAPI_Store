"""src/domain/constants/orders.py"""

from enum import Enum

__all__ = ("OrderStatus",)


class OrderStatus(Enum):
    """Values for Order status"""

    PENDING = "PENDING"
    PAID = "PAID"
    SHIPPED = "SHIPPED"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"
