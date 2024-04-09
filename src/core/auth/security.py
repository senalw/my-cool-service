from datetime import datetime, timedelta
from typing import Optional

from dependency_injector.wiring import inject, Provide
from fastapi import Depends
from jose import jwt
from pydantic import ValidationError
from src.core.container import Container
from src.core.exception import AuthenticationError
from src.domain.user_dto import UserDomain
from src.schema import Payload
from src.util.utils import verify_password


@inject
def create_access_token(
    subject: dict,
    expires_delta: timedelta = None,
    configs=Depends(Provide[Container.configs]),  # noqa B008
) -> str:
    if expires_delta:
        expire = datetime.now().timestamp() + expires_delta.total_seconds()
    else:
        expire = (
            datetime.now().timestamp()
            + timedelta(
                minutes=configs.security_config.token_expiration_time
            ).total_seconds()
        )
    payload = {"exp": expire, **subject}
    encoded_jwt = jwt.encode(
        claims=payload,
        key=configs.security_config.secret_key,
        algorithm=configs.security_config.algorithm,
    )

    return encoded_jwt


@inject
def decode_token(
    token: str, configs=Depends(Provide[Container.configs])  # noqa B008
) -> Optional[Payload]:
    try:
        payload = jwt.decode(
            token=token,
            key=configs.security_config.secret_key,
            algorithms=configs.security_config.algorithm,
        )
        return (
            Payload(**payload)
            if payload.get("exp", 0) >= int(round(datetime.utcnow().timestamp()))
            else None
        )
    except (AttributeError, jwt.JWTError, ValidationError):
        raise AuthenticationError("Token is invalid")


@inject
def authenticate_user(
    username: str,
    password: str,
    user_repo=Depends(Provide[Container.user_repository]),  # noqa B008
) -> Optional[UserDomain]:
    user: Optional[UserDomain] = user_repo.get_user_by_id(username)
    if not user or not verify_password(password, user.password):
        raise AuthenticationError("Invalid username or password")
    return user
