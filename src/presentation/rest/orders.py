"""src/presentation/rest/orders.py"""

from fastapi import APIRouter, Depends, HTTPException, Request, status

from src.application.authentication import get_current_user
from src.domain.constants import OrderStatus
from src.domain.orders import (
    Order,
    OrderCreateRequestBody,
    OrderPublic,
    OrdersRepository,
    OrderUncommited,
)
from src.domain.products import Product, ProductRepository
from src.domain.users import User
from src.infrastructure.database.transaction import transaction
from src.infrastructure.models import Response, ResponseMulti

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("/add_to_cart", status_code=status.HTTP_201_CREATED)
@transaction
async def cart_create(
    _: Request,
    schema: OrderCreateRequestBody,
    user: User = Depends(get_current_user),
) -> Response[OrderPublic]:
    """Add product to cart"""

    # Get the product from database to check product`s amount
    product = await ProductRepository().get(
        key_="id", value_=schema.product_id
    )
    if product.amount < schema.amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"Not enough quantity, there are "
                f"{product.amount} pieces in stock"
            ),
        )

    # Create new order with 'PENDING' status
    order_raw = OrderUncommited(
        product_id=schema.product_id,
        amount=schema.amount,
        user_id=user.id,
        delivery_address=user.address,
    )

    # Add order to the database like in cart
    order: Order = await OrdersRepository().create(schema=order_raw)
    order_public = OrderPublic.from_orm(order)

    return Response[OrderPublic](result=order_public)


@router.get("/my_cart", status_code=status.HTTP_200_OK)
@transaction
async def cart_list(
    _: Request,
    skip: int = None,
    limit: int = None,
    user: User = Depends(get_current_user),  # pylint: disable=W0613
) -> ResponseMulti[OrderPublic]:
    """Get all orders from my cart."""

    # Get all user`s products with 'PENDING' status from the database
    orders_public = [
        OrderPublic.from_orm(order)
        async for order in OrdersRepository().all_pending(
            value_=user.id, skip_=skip, limit_=limit
        )
    ]

    return ResponseMulti[OrderPublic](result=orders_public)


@router.put("/my_cart", status_code=status.HTTP_202_ACCEPTED)
@transaction
async def product_amount_update(
    _: Request,
    order_id: int,
    new_amount: int,
    user: User = Depends(get_current_user),  # pylint: disable=W0613
) -> Response[OrderPublic]:
    """Update product amount"""

    # Get the order from database
    order = await OrdersRepository().get(key_="id", value_=order_id)

    # Check the status of the order
    if order.status != "PENDING":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Order status is not pending",
        )

    # Update products amount
    payload = {"amount": new_amount}
    product: Order = await OrdersRepository().update(
        key_="id", value_=order_id, payload_=payload
    )
    product_public = OrderPublic.from_orm(product)

    return Response[OrderPublic](result=product_public)


@router.delete("/my_cart")
@transaction
async def cart_remove(
    _: Request,
    order_id: int,
    user: User = Depends(get_current_user),  # pylint: disable=W0613
):
    """Delete unpayed order from cart"""

    # Get the product from database to check product`s status
    order = await OrdersRepository().get(key_="id", value_=order_id)
    if order.status != "PENDING":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bad Request",
        )

    # Delete order from database
    await OrdersRepository().delete(id_=order_id)

    return HTTPException(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/pay_my_cart", status_code=status.HTTP_202_ACCEPTED)
@transaction
async def order_pay(
    _: Request,
    skip: int = None,
    limit: int = None,
    user: User = Depends(get_current_user),
):
    """Pay products from cart"""

    # Creating products list from orders with status PENDING
    product_list = [
        Order.from_orm(order)
        async for order in OrdersRepository().all_pending(
            value_=user.id, skip_=skip, limit_=limit
        )
    ]

    # Update products amount in products database table
    for order in product_list:
        product: Product = await ProductRepository().get(
            key_="id", value_=order.product_id
        )
        if product.amount >= order.amount:
            product.amount -= order.amount
            await ProductRepository().update(
                key_="id",
                value_=product.id,
                payload_={"amount": product.amount},
            )
        else:
            order.amount = product.amount
            product.amount = 0
            await OrdersRepository().update(
                key_="id", value_=order.id, payload_={"amount": order.amount}
            )
            await ProductRepository().update(
                key_="id",
                value_=product.id,
                payload_={"amount": product.amount},
            )
        # Update order status
        await OrdersRepository().update(
            key_="id", value_=order.id, payload_={"status": OrderStatus.PAID}
        )

    # Add updated orders id to list
    orders_id = [order.id for order in product_list]

    # Get updated orders
    updated_orders = []
    for order_id in orders_id:
        order: Order = await OrdersRepository().get(key_="id", value_=order_id)
        updated_orders.append(order)

    orders_public = [OrderPublic.from_orm(order) for order in updated_orders]

    # TODO add celery function to send manager email with orders_public copy

    return ResponseMulti[OrderPublic](result=orders_public)
