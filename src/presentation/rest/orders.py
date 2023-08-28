"""src/presentation/rest/orders.py"""

from fastapi import APIRouter, Depends, HTTPException, Request, status

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
from src.infrastructure.models import Response, ResponseMulti

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


@router.get("/my_cart", status_code=status.HTTP_200_OK)
@transaction
async def cart_list(
    _: Request,
    skip: int,
    limit: int,
    user: User = Depends(get_current_user),  # pylint: disable=W0613
) -> ResponseMulti[OrderPublic]:
    """Get all orders from my cart."""

    # Get all my products from the cart
    orders_public = [
        OrderPublic.from_orm(order)
        async for order in OrdersRepository().all_my_catr(user.id, skip, limit)
    ]

    return ResponseMulti[OrderPublic](result=orders_public)


@router.delete("/my_cart")
@transaction
async def cart_remove(
    _: Request,
    order_id: int,
    user: User = Depends(get_current_user),  # pylint: disable=W0613
):
    """Delete unpayed order from cart"""

    # Delete order from database
    await OrdersRepository().delete(id_=order_id)

    return HTTPException(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/my_cart", status_code=status.HTTP_202_ACCEPTED)
@transaction
async def product_amount_update(
    _: Request,
    order_id: int,
    new_amount: int,
    user: User = Depends(get_current_user),  # pylint: disable=W0613
) -> Response[OrderPublic]:
    """Update product amount, only managers"""

    # Update products amount
    payload = {"amount": new_amount}
    product: Order = await OrdersRepository().update(
        key_="id", value_=order_id, payload_=payload
    )
    product_public = OrderPublic.from_orm(product)

    return Response[OrderPublic](result=product_public)
