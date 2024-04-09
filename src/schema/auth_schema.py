from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class Payload(BaseModel):
    id: int
    username: str
    is_admin: bool
