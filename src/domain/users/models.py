"""src/domain/users/models.py"""

from pydantic import EmailStr

from src.infrastructure.models import InternalModel

__all__ = ("UserUncommited", "User")


# Internal models
# ------------------------------------------------------
class UserUncommited(InternalModel):
    """This schema is used for creating instance in the database."""

    email: EmailStr
    phone_number: str
    password: str
    first_name: str
    last_name: str


class User(UserUncommited):
    """Existed product representation."""

    id: int
    is_manager: bool
