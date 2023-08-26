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


@router.post("/cteate", status_code=status.HTTP_201_CREATED)
@transaction
async def user_create(
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
async def user_me(
    current_user: UserPublic = Depends(get_current_user),
) -> dict:
    """Function return current user"""

    user = current_user.dict()
    user.pop("password")
    return Response[UserPublic](result=user)


@router.get("/list", status_code=status.HTTP_200_OK)
@transaction
async def users_all(
    user=Depends(RoleRequired(True)), skip: int = 0, limit: int = 5
) -> ResponseMulti[UserPublic]:
    """Function return allusers, only for managers"""

    users_list = [
        UserPublic.from_orm(users)
        async for users in UsersRepository().all(skip=skip, limit=limit)
    ]

    return ResponseMulti[UserPublic](result=users_list)


@router.put("/manager", status_code=status.HTTP_202_ACCEPTED)
@transaction
async def user_manager(
    schema: UserPublic = Depends(get_current_user),
) -> dict:
    """Function updated user to user-manager"""

    schema.is_manager = True
    user: UserPublic = await UsersRepository().update(
        id_=schema.id, schema=schema
    )
    manager = user.dict()
    manager.pop("password")
    return Response[UserPublic](result=manager)
