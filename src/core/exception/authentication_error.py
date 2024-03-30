from fastapi import status
from src.core.exception import MyCoolServiceError


class AuthenticationError(MyCoolServiceError):
    def __init__(
        self, message: str, code: status = status.HTTP_401_UNAUTHORIZED
    ) -> None:
        super().__init__(message, code)
        self.message = message
        self.code = code

    def __str__(self) -> str:
        return f"Authentication Error: {self.message}"
