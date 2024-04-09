from dependency_injector.wiring import inject
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from src.core.auth.security import authenticate_user, create_access_token

router = APIRouter(prefix="/auth")


@router.post("/token")
@inject
async def sign_in(
    form_data: OAuth2PasswordRequestForm = Depends(),  # noqa B008
) -> dict:
    user = authenticate_user(form_data.username, form_data.password)
    subject = {
        "id": user.user_id,
        "username": form_data.username,
        "is_admin": user.is_admin,
    }
    access_token = create_access_token(subject=subject)
    return {"access_token": access_token, "token_type": "bearer"}
