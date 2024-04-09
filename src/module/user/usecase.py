from typing import List

from src.core import UseCase
from src.core.exception import InvalidArgumentError
from src.domain import UserModel
from src.domain.user_dto import UserDomain
from src.module.user import UserRepository
from src.module.user.mapper import UserMapper
from src.schema import GetUserOutputSchema, ListUsersResponse, Request


class CreateUserUseCase(UseCase):
    def __init__(self, user_repo: UserRepository) -> None:
        self.user_repo: UserRepository = user_repo

    def execute(self, request: Request) -> GetUserOutputSchema:

        if not request.username:
            raise InvalidArgumentError("Username can't be empty")
        if not request.password:
            raise InvalidArgumentError("Password can't be empty")

        user_model: UserModel = UserMapper.to_persistent(request)
        self.user_repo.add_user(user_model)
        return GetUserOutputSchema(username=user_model.username, email=user_model.email)


class ListUsersUseCase(UseCase):
    def __init__(self, user_repo: UserRepository) -> None:
        self.user_repo: UserRepository = user_repo

    def execute(self, request: Request = None) -> ListUsersResponse:
        users: List[UserDomain] = self.user_repo.get_users()
        users_response: List[GetUserOutputSchema] = [
            GetUserOutputSchema(username=user_dto.username, email=user_dto.email)
            for user_dto in users
        ]
        return ListUsersResponse(users=users_response)
