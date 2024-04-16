import logging

from dependency_injector.wiring import inject
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from src.core.auth.security import authenticate_user, create_access_token
from src.schema import Token

router = APIRouter(prefix="/auth")


@router.post("/token", response_model=Token)
@inject
async def sign_in(
    form_data: OAuth2PasswordRequestForm = Depends(),  # noqa B008
) -> Token:
    user = authenticate_user(form_data.username, form_data.password)
    subject = {
        "id": user.user_id,
        "username": form_data.username,
        "is_admin": user.is_admin,
    }
    access_token = create_access_token(subject=subject)
    logging.info(f"{form_data.username} logged in")
    return Token(access_token=access_token, token_type="bearer")  # noqa S106
