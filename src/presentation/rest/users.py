"""src/presentation/rest/users.py"""

from fastapi import APIRouter, Depends, Request, status

from src.application.authentication import RoleRequired, get_current_user
from src.config import pwd_context
from src.domain.users import (
    User,
    UserCreateRequestBody,
    UserPublic,
    UsersRepository,
    UserUncommited,
)
from src.infrastructure.database.transaction import transaction
from src.infrastructure.models import Response, ResponseMulti

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/create", status_code=status.HTTP_201_CREATED)
@transaction
async def user_create(
    _: Request,
    schema: UserCreateRequestBody,
) -> Response[UserPublic]:
    """Create new user."""

    # Password hashing
    hashed_password = pwd_context.hash(schema.password)
    schema.password = hashed_password

    # Save new user to the database
    user: User = await UsersRepository().create(
        UserUncommited(**schema.dict())
    )
    user_public = UserPublic.from_orm(user)

    return Response[UserPublic](result=user_public)


@router.get("/me", status_code=status.HTTP_200_OK)
@transaction
async def user_me(
    current_user: User = Depends(get_current_user),
) -> Response[UserPublic]:
    """Get current aythenticate user by JWT token"""

    # Get user by JWT from database
    user: User = await UsersRepository().get(key_="id", value_=current_user.id)
    user_public = UserPublic.from_orm(user)

    return Response[UserPublic](result=user_public)


@router.get("/list", status_code=status.HTTP_200_OK)
@transaction
async def users_all(
    _: User = Depends(RoleRequired(True)),
    skip: int = None,
    limit: int = None,
) -> ResponseMulti[UserPublic]:
    """Function return all users, only for managers"""

    # Get users list from database
    users_list = [
        UserPublic.from_orm(users)
        async for users in UsersRepository().all(skip_=skip, limit_=limit)
    ]

    return ResponseMulti[UserPublic](result=users_list)


@router.put("/manager", status_code=status.HTTP_202_ACCEPTED)
@transaction
async def user_manager(
    user: UserPublic = Depends(get_current_user),
) -> Response[UserPublic]:
    """Update user to user-manager"""

    # Update user to user-manager
    user.is_manager = True
    user: User = await UsersRepository().update(
        key_="id", value_=user.id, payload_=user
    )
    manager = UserPublic.from_orm(user)

    return Response[UserPublic](result=manager)
