from src.module.user import UserRepository
from src.module.user.usecase import CreateUserUseCase, ListUsersUseCase
from src.schema import AddUserInputSchema, GetUserOutputSchema, ListUsersResponse


class UserService:
    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository: UserRepository = user_repository

    def create_user(self, user: AddUserInputSchema) -> GetUserOutputSchema:
        return CreateUserUseCase(self.user_repository).execute(user)

    def get_users(self) -> ListUsersResponse:
        return ListUsersUseCase(self.user_repository).execute()
