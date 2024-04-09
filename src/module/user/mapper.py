from src.domain import UserModel
from src.domain.user_dto import UserDomain
from src.schema import AddUserInputSchema
from src.util.utils import get_hashed_password


class UserMapper:
    @staticmethod
    def to_domain(user_model: UserModel) -> UserDomain:
        return UserDomain(
            user_id=user_model.user_id,
            username=user_model.username,
            password=user_model.password,
            email=user_model.email,
            is_admin=user_model.is_admin,
        )

    @staticmethod
    def to_persistent(user_schema: AddUserInputSchema) -> UserModel:
        return UserModel(
            username=user_schema.username,
            email=user_schema.email if user_schema.email else None,
            password=get_hashed_password(user_schema.password.get_secret_value()),
            is_admin=user_schema.is_admin,
        )
