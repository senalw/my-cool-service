from dependency_injector import containers, providers
from src.config.config import Config
from src.core.database.postgres_client import PostgresClient
from src.service import OrderService, ProductService

from src.module.user import UserRepositoryImpl


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "src.api.v1.endpoints.user",
        ]
    )

    conf: Config = Config.get_instance()
    db = providers.Singleton(PostgresClient, configs=conf.db_configs)

    user_repository = providers.Factory(UserRepositoryImpl)

    product_service = providers.Factory(
        ProductService, database=db, user_repository=user_repository
    )

    order_service = providers.Factory(
        OrderService,
        database=db,
        user_repository=user_repository,
    )
