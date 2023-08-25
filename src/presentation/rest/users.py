"""src/presentation/rest/users.py"""

from fastapi import APIRouter, Depends, Request, status

from src.application.authentication import get_current_user
from src.config import pwd_context
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

    # Password hashing
    hashed_password = pwd_context.hash(schema.password)
    schema.password = hashed_password

    # Save user to the database
    user: User = await UsersRepository().create(
        UserUncommited(**schema.dict())
    )
    user_public = UserPublic.from_orm(user)

    return Response[UserPublic](result=user_public)


@router.get("/me", status_code=status.HTTP_200_OK)
@transaction
async def users_me(current_user: User = Depends(get_current_user)) -> dict:
    """Function return current user"""

    return current_user.dict()
