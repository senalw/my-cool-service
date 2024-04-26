from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from src.core.container import Container
from src.module.user import UserService
from src.schema import AddUserInputSchema, GetUserOutputSchema, ListUsersResponse
from starlette import status

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    dependencies=[Depends(Container.oauth2_password_bearer)],
)


@router.post(
    "", status_code=status.HTTP_201_CREATED, response_model=GetUserOutputSchema
)
@inject
async def create_user(
    request: AddUserInputSchema,
    user_service: UserService = Depends(Provide[Container.user_service]),  # noqa B008
) -> GetUserOutputSchema:
    return user_service.create_user(request)


@router.get("", status_code=status.HTTP_200_OK, response_model=ListUsersResponse)
@inject
async def get_users(
    user_service: UserService = Depends(Provide[Container.user_service]),  # noqa B008
) -> ListUsersResponse:
    return user_service.get_users()
