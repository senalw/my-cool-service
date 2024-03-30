from fastapi import status
from src.core.exception.auto_cart_service_error import MyCoolServiceError


class InvalidArgumentError(MyCoolServiceError):
    def __init__(
        self, message: str, code: status = status.HTTP_422_UNPROCESSABLE_ENTITY
    ) -> None:
        super().__init__(message, code)
        self.message = message
        self.code = code

    def __str__(self) -> str:
        return f"Invalid Argument Error: {self.message}"
