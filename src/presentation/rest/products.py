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
async def product_by_id(_: Request, product_id: int) -> ProductPublic:
    """Get product by product id"""

    # Get product from database by id
    product_public: ProductPublic = await ProductRepository().get(
        id_=product_id
    )

    return product_public


@router.get("/name/{name}", status_code=status.HTTP_200_OK)
@transaction
async def product_by_name(_: Request, name: str) -> ProductPublic | None:
    """Get product by product name"""

    # Get product from database by name
    product_public: ProductPublic = await ProductRepository().get_by_name(
        name_=name
    )

    return product_public


@router.get("/all", status_code=status.HTTP_200_OK)
@transaction
async def products_list(
    _: Request, skip: int = 0, limit: int = 5
) -> ResponseMulti[ProductPublic]:
    """Get all my products."""

    # Get all products from the database
    products_public = [
        ProductPublic.from_orm(product)
        async for product in ProductRepository().all(skip=skip, limit=limit)
    ]

    return ResponseMulti[ProductPublic](result=products_public)


@router.post("/add", status_code=status.HTTP_201_CREATED)
@transaction
async def product_create(
    _: Request,
    schema: ProductCreateRequestBody,
    user: User = Depends(RoleRequired(True)),
) -> Response[ProductPublic]:
    """Create a new product, only managers"""

    # Save product to the database
    product: Product = await ProductRepository().create(
        ProductUncommited(**schema.dict())
    )
    product_public = ProductPublic.from_orm(product)

    return Response[ProductPublic](result=product_public)
