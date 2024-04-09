from passlib.context import CryptContext


def get_hashed_password(password: str) -> str:
    return CryptContext(schemes=["bcrypt"], deprecated="auto").hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return CryptContext(schemes=["bcrypt"], deprecated="auto").verify(
        plain_password, hashed_password
    )
