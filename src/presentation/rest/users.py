"""src/presentation/rest/users.py"""

from fastapi import APIRouter, Request, status

from src.domain.users import (
    User,
    UserCreateRequestBody,
    UserPublic,
    UsersRepository,
    UserUncommited,
)
from src.infrastructure.database.transaction import transaction
from src.infrastructure.models import Response

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("", status_code=status.HTTP_201_CREATED)
@transaction
async def users_create(
    _: Request,
    schema: UserCreateRequestBody,
) -> Response[UserPublic]:
    """Create a new usser."""

    # Save user to the database
    user: User = await UsersRepository().create(
        UserUncommited(**schema.dict())
    )
    user_public = UserPublic.from_orm(user)

    return Response[UserPublic](result=user_public)
