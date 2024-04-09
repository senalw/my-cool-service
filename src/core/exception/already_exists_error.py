from fastapi import status
from src.core.exception.my_cool_service_error import MyCoolServiceError


class AlreadyExistsError(MyCoolServiceError):
    def __init__(self, message: str, code: status = status.HTTP_409_CONFLICT) -> None:
        super().__init__(message, code)
        self.message = message
        self.code = code

    def __str__(self) -> str:
        return f"Resource Already Exists: {self.message}"
