"""src/presentation/rest/products.py"""

from fastapi import APIRouter, Depends, HTTPException, Request, status

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
async def product_by_id(
    _: Request, product_id: int
) -> Response[ProductPublic]:
    """Get product by product id from database"""

    # Get product from database by id
    product: Product = await ProductRepository().get(
        key_="id", value_=product_id
    )
    product_public = ProductPublic.from_orm(product)

    return Response[ProductPublic](result=product_public)


@router.get("/name/{name}", status_code=status.HTTP_200_OK)
@transaction
async def product_by_name(_: Request, name: str) -> Response[ProductPublic]:
    """Get product by product name from database"""

    # Get product from database by name
    product: Product = await ProductRepository().get(key_="name", value_=name)
    product_public = ProductPublic.from_orm(product)

    return Response[ProductPublic](result=product_public)


@router.get("/all", status_code=status.HTTP_200_OK)
@transaction
async def products_list(
    _: Request, skip: int = None, limit: int = None
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
    product: ProductCreateRequestBody,
    user: User = Depends(RoleRequired(True)),  # pylint: disable=W0613
) -> Response[ProductPublic]:
    """Create a new product, only managers"""

    # Save product to the database
    added_product: Product = await ProductRepository().create(
        ProductUncommited(**product.dict())
    )
    product_public = ProductPublic.from_orm(added_product)

    return Response[ProductPublic](result=product_public)


@router.put("/update_name", status_code=status.HTTP_202_ACCEPTED)
@transaction
async def product_name_update(
    _: Request,
    product_id: int,
    new_name: str,
    user: User = Depends(RoleRequired(True)),  # pylint: disable=W0613
) -> Response[ProductPublic]:
    """Update product name, only managers"""

    # Update products name
    payload = {"name": new_name}
    product: Product = await ProductRepository().update(
        key_="id", value_=product_id, payload_=payload
    )
    product_public = ProductPublic.from_orm(product)

    return Response[ProductPublic](result=product_public)


@router.put("/update_title", status_code=status.HTTP_202_ACCEPTED)
@transaction
async def product_title_update(
    _: Request,
    product_id: int,
    new_title: str,
    user: User = Depends(RoleRequired(True)),  # pylint: disable=W0613
) -> Response[ProductPublic]:
    """Update product title, only managers"""

    # Update products title
    payload = {"title": new_title}
    product: Product = await ProductRepository().update(
        key_="id", value_=product_id, payload_=payload
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

    # Update products price
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

    # Update products amount
    payload = {"amount": new_amount}
    product: Product = await ProductRepository().update(
        key_="id", value_=product_id, payload_=payload
    )
    product_public = ProductPublic.from_orm(product)

    return Response[ProductPublic](result=product_public)


@router.delete("/remove")
@transaction
async def product_remove(
    _: Request,
    product_id: int,
    user: User = Depends(RoleRequired(True)),  # pylint: disable=W0613
):
    """Delete product from database, only managers"""

    # Delete product from database
    await ProductRepository().delete(id_=product_id)

    return HTTPException(status_code=status.HTTP_204_NO_CONTENT)
