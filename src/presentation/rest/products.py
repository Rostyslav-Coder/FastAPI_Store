"""src/presentation/rest/products.py"""

from fastapi import APIRouter, Depends, Request, status

from src.application.authentication import RoleRequired
from src.domain.products import (
    Product,
    ProductCreateRequestBody,
    ProductPublic,
    ProductRepository,
    ProductUncommited,
)
from src.domain.users import User
from src.infrastructure.database.transaction import transaction
from src.infrastructure.models import Response, ResponseMulti

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/id/{product_id}", status_code=status.HTTP_200_OK)
@transaction
async def product_by_id(_: Request, prdct_id: int) -> Response[ProductPublic]:
    """Get product by product id from DB"""

    # Get product from database by id
    product: Product = await ProductRepository().get(id_=prdct_id)
    product_public = ProductPublic.from_orm(product)

    return Response[ProductPublic](result=product_public)


@router.get("/name/{name}", status_code=status.HTTP_200_OK)
@transaction
async def product_by_name(_: Request, name: str) -> Response[ProductPublic]:
    """Get product by product name from DB"""

    # Get product from database by name
    product: Product = await ProductRepository().get_by_name(name_=name)
    product_public = ProductPublic.from_orm(product)

    return Response[ProductPublic](result=product_public)


@router.get("/all", status_code=status.HTTP_200_OK)
@transaction
async def products_list(
    _: Request, skip: int = 0, limit: int = 5
) -> ResponseMulti[ProductPublic]:
    """Get all products from DB"""

    # Get all products from the database
    products_public = [
        ProductPublic.from_orm(product)
        async for product in ProductRepository().all(skip_=skip, limit_=limit)
    ]

    return ResponseMulti[ProductPublic](result=products_public)


@router.post("/add", status_code=status.HTTP_201_CREATED)
@transaction
async def product_create(
    _: Request,
    schema: ProductCreateRequestBody,
    user: User = Depends(RoleRequired(True)),  # pylint: disable=W0613
) -> Response[ProductPublic]:
    """Create a new product, only managers"""

    # Save product to the database
    product: Product = await ProductRepository().create(
        ProductUncommited(**schema.dict())
    )
    product_public = ProductPublic.from_orm(product)

    return Response[ProductPublic](result=product_public)


@router.put("/update_price", status_code=status.HTTP_202_ACCEPTED)
@transaction
async def product_price_update(
    _: Request,
    product_id: int,
    new_price: int,
    user: User = Depends(RoleRequired(True)),  # pylint: disable=W0613
) -> Response[ProductPublic]:
    """Update product price, only managers"""

    payload = {"price": new_price}
    product: Product = await ProductRepository().update(
        key_="id", value_=product_id, payload_=payload
    )
    product_public = ProductPublic.from_orm(product)

    return Response[ProductPublic](result=product_public)


@router.put("/update_amount", status_code=status.HTTP_202_ACCEPTED)
@transaction
async def product_amount_update(
    _: Request,
    product_id: int,
    new_amount: int,
    user: User = Depends(RoleRequired(True)),  # pylint: disable=W0613
) -> Response[ProductPublic]:
    """Update product amount, only managers"""

    payload = {"amount": new_amount}
    product: Product = await ProductRepository().update(
        key_="id", value_=product_id, payload_=payload
    )
    product_public = ProductPublic.from_orm(product)

    return Response[ProductPublic](result=product_public)
