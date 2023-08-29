"""src/application/authentication/dependency_injection.py"""

from datetime import datetime, timedelta

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import ValidationError

from src.config import settings
from src.domain.authentication import TokenPayload
from src.domain.users import User, UsersRepository
from src.infrastructure.errors import AuthenticationError, AuthorizationError

__all__ = (
    "get_current_user",
    "create_access_token",
    "RoleRequired",
)

oauth2_oauth = OAuth2PasswordBearer(
    tokenUrl="/auth/openapi",
    scheme_name=settings.authentication.scheme,
)


async def get_current_user(token: str = Depends(oauth2_oauth)) -> User:
    """Function return current user"""

    try:
        payload = jwt.decode(
            token,
            settings.authentication.access_token.secret_key,
            algorithms=[settings.authentication.algorithm],
        )
        token_payload = TokenPayload(**payload)

        if datetime.fromtimestamp(token_payload.exp) < datetime.now():
            raise AuthenticationError
    except (JWTError, ValidationError):
        raise AuthenticationError  # pylint: disable=W0707

    user = await UsersRepository().get(key_="id", value_=token_payload.sub)

    return user


def create_access_token(data: dict) -> str:
    """function create & return access token"""

    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(
        seconds=settings.authentication.access_token.ttl
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.authentication.access_token.secret_key,
        algorithm=settings.authentication.algorithm,
    )
    return encoded_jwt


class RoleRequired:
    """Require users role"""

    def __init__(self, role: bool):
        self.is_manager = role

    async def __call__(self, user: User = Depends(get_current_user)):
        if user.is_manager != self.is_manager:
            raise AuthorizationError

        return user
