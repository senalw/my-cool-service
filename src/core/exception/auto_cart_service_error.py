from fastapi import HTTPException, status


class MyCoolServiceError(HTTPException):
    def __init__(self, message: str, code: status) -> None:
        super().__init__(status_code=code, detail=message)
        self.status_code = code
        self.detail = message
