from fastapi import status
from src.core.exception import MyCoolServiceError


class NotFoundError(MyCoolServiceError):
    def __init__(self, message: str, code: status = status.HTTP_404_NOT_FOUND) -> None:
        super().__init__(message, code)
        self.message = message
        self.code = code

    def __str__(self) -> str:
        return f"Not Found Error: {self.message}"
