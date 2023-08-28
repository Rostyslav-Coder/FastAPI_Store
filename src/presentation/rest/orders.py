"""src/presentation/rest/orders.py"""

from fastapi import APIRouter, Depends, Request, status

from src.application.authentication import get_current_user
from src.domain.orders import (
    Order,
    OrderCreateRequestBody,
    OrderPublic,
    OrdersRepository,
    OrderUncommited,
)
from src.domain.users import User
from src.infrastructure.database.transaction import transaction
from src.infrastructure.models import Response

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("/add_to_cart", status_code=status.HTTP_201_CREATED)
@transaction
async def order_create(
    _: Request,
    schema: OrderCreateRequestBody,
    user: User = Depends(get_current_user),
) -> Response[OrderPublic]:
    """Create a new pre-order."""

    order_raw = OrderUncommited(
        product_id=schema.product_id,
        amount=schema.amount,
        user_id=user.id,
        delivery_address=user.address,
    )

    # Save user to the database
    order: Order = await OrdersRepository().create(schema=order_raw)
    order_public = OrderPublic.from_orm(order)

    return Response[OrderPublic](result=order_public)
