"""src/presentation/rest/authentication.py"""

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from src.application.authentication import create_access_token
from src.config import settings
from src.domain.users import UsersRepository
from src.infrastructure.errors import NotFoundError

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Authenticate user"""

    # Get user from the database by email in place of username
    user = await UsersRepository().get(key_="email", value_=form_data.username)

    if not user:
        raise NotFoundError

    # Creating user token
    access_token = create_access_token(data={"sub": str(user.id)})

    return {
        "access_token": access_token,
        "token_type": settings.authentication.scheme,
    }
