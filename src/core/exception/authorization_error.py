from src.core.exception.my_cool_service_error import MyCoolServiceError
from starlette import status


class AuthorizationError(MyCoolServiceError):
    def __init__(self, message: str, code: status = status.HTTP_403_FORBIDDEN) -> None:
        super().__init__(message, code)
        self.message = message
        self.code = code

    def __str__(self) -> str:
        return f"Authorization Error: {self.message}"
