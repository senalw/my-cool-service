from dataclasses import dataclass


@dataclass
class UserDomain:
    user_id: int
    username: str
    password: str
    email: str
    is_admin: bool
