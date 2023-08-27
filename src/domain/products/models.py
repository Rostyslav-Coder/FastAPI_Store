"""src/domain/products/models.py"""

from pydantic import Field

from src.infrastructure.models import InternalModel, PublicModel

__all__ = (
    "ProductCreateRequestBody",
    "ProductPublic",
    "ProductUncommited",
    "Product",
)


# Public models
# ------------------------------------------------------
class _ProductPublic(PublicModel):
    name: str = Field(description="OpenAPI description")
    title: str = Field(description="OpenAPI description")
    price: int = Field(description="OpenAPI description")
    amount: int = Field(description="OpenAPI description")


class ProductCreateRequestBody(_ProductPublic):
    """Product create request body."""

    pass  # pylint: disable=W0107


class ProductPublic(_ProductPublic):
    """The internal application representation."""

    id: int


# Internal models
# ------------------------------------------------------
class _ProductInternal(InternalModel):
    name: str
    title: str
    price: int
    amount: int


class ProductUncommited(_ProductInternal):
    """This schema is used for creating instance in the database."""

    pass  # pylint: disable=W0107


class Product(_ProductInternal):
    """Existed product representation."""

    id: int
