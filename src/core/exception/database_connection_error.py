from fastapi import status
from src.core.exception.auto_cart_service_error import MyCoolServiceError


class DatabaseConnectionError(MyCoolServiceError):
    def __init__(
        self, message: str, code: status = status.HTTP_503_SERVICE_UNAVAILABLE
    ) -> None:
        super().__init__(message, code)
        self.message = message
        self.code = code

    def __str__(self) -> str:
        return f"Database Connection Error: {self.message}"
