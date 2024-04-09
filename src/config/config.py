from configparser import ConfigParser

from settings import ROOT_DIR
from src.config.env_interpolation import EnvInterpolation


class Config:
    def __init__(self) -> None:
        config_parser: ConfigParser = ConfigParser(
            interpolation=EnvInterpolation()
        )  # noqa E501
        config_parser.read(f"{ROOT_DIR}/resources/config.ini")
        self.db_configs: Config.DatabaseConfig = Config.DatabaseConfig(
            config_parser
        )  # noqa E501
        self.project_config: Config.ProjectConfig = Config.ProjectConfig(
            config_parser
        )  # noqa E501
        self.security_config: Config.SecurityConfig = Config.SecurityConfig(
            config_parser
        )  # noqa E501

    class DatabaseConfig:
        def __init__(self, configs: ConfigParser) -> None:
            self.db_url: str = configs.get("Database", "DB_URL")

    class ProjectConfig:
        def __init__(self, configs: ConfigParser) -> None:
            self.name: str = configs.get("Project", "NAME")
            self.api: str = configs.get("Project", "API")
            self.version: str = configs.get("Project", "VERSION")

    class SecurityConfig:
        def __init__(self, configs: ConfigParser) -> None:
            self.secret_key = configs.get("SECURITY", "SECRET_KEY")
            self.algorithm = configs.get("SECURITY", "ALGORITHM")
            self.token_url = configs.get("SECURITY", "TOKEN_URL")
            self.token_expiration_time = configs.getint(
                "SECURITY", "TOKEN_EXPIRATION_TIME"
            )
            self.datatime_format = configs.get("SECURITY", "DATETIME_FORMAT")
            self.opa_url = configs.get("SECURITY", "OPA_URL")
