import string
from typing import List

from pydantic import EmailStr, field_validator, SecretStr
from src.core.exception import RequestValidationError
from src.schema import Request, Response


class AddUserInputSchema(Request):
    username: str
    email: EmailStr | None
    password: SecretStr
    is_admin: bool

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: SecretStr) -> SecretStr:  # noqa ANN102
        password = value.get_secret_value()
        min_len = 8
        if len(password) < min_len:
            raise RequestValidationError("Password must be at least 8 characters long")
        if not any(character.isupper() for character in password):
            raise RequestValidationError(
                "Password should contain at least one uppercase character"
            )
        if not any(character in string.punctuation for character in password):
            raise RequestValidationError(
                "Password must contain at least one special character"
            )
        return value


class GetUserInputSchema(Request):
    username: str
    email: str


class GetUserOutputSchema(Response):
    username: str
    email: str


class ListUsersResponse(Response):
    users: List[GetUserOutputSchema]
