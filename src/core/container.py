from dependency_injector import containers, providers
from fastapi.security import OAuth2PasswordBearer
from src.config.config import Config
from src.core.database.postgres_client import PostgresClient
from src.module.user import UserRepositoryImpl, UserService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "src.api.v1.endpoints.auth",
            "src.api.v1.endpoints.user",
            "src.core.auth.security",
            "src.core.auth.auth_interceptor",
        ]
    )

    configs = providers.Singleton(Config)
    db = providers.Singleton(PostgresClient, configs=configs)
    user_repository = providers.Factory(UserRepositoryImpl, db=db)
    user_service = providers.Factory(UserService, user_repository=user_repository)
    oauth2_password_bearer = OAuth2PasswordBearer(
        tokenUrl=configs().security_config.token_url
    )
