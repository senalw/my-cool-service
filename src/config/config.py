import logging
from configparser import ConfigParser
from typing import List

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
        self.app_config: Config.AppConfig = Config.AppConfig(config_parser)  # noqa E501
        self.security_config: Config.SecurityConfig = Config.SecurityConfig(
            config_parser
        )  # noqa E501

        missing_configs: List[str] = self.__validate_configs()
        if missing_configs:
            logging.error(f"Missing Configs: {missing_configs}")

    def __validate_configs(self) -> List[str]:
        missing_configs = []
        if not self.db_configs.db_url:
            missing_configs.append("DB_URL")
        if not self.app_config.name:
            missing_configs.append("NAME")
        if not self.app_config.api:
            missing_configs.append("API")
        if not self.app_config.version:
            missing_configs.append("VERSION")
        if not self.app_config.port:
            missing_configs.append("PORT")
        if not self.security_config.secret_key:
            missing_configs.append("SECRET_KEY")
        if not self.security_config.algorithm:
            missing_configs.append("ALGORITHM")
        if not self.security_config.token_url:
            missing_configs.append("TOKEN_URL")
        if not self.security_config.token_expiration_time:
            missing_configs.append("TOKEN_EXPIRATION_TIME")
        if not self.security_config.datatime_format:
            missing_configs.append("DATETIME_FORMAT")
        if not self.security_config.opa_url:
            missing_configs.append("OPA_URL")
        if not self.security_config.opa_public_key:
            missing_configs.append("OPA_PUBLIC_KEY")

        return missing_configs

    class DatabaseConfig:
        def __init__(self, configs: ConfigParser) -> None:
            self.db_url: str = configs.get("Database", "DB_URL")

    class AppConfig:
        def __init__(self, configs: ConfigParser) -> None:
            self.name: str = configs.get("APP", "NAME")
            self.api: str = configs.get("APP", "API")
            self.version: str = configs.get("APP", "VERSION")
            self.port: int = configs.getint("APP", "PORT")

    class SecurityConfig:
        def __init__(self, configs: ConfigParser) -> None:
            self.secret_key: str = configs.get("SECURITY", "SECRET_KEY")
            self.algorithm: str = configs.get("SECURITY", "ALGORITHM")
            self.token_url: str = configs.get("SECURITY", "TOKEN_URL")
            self.token_expiration_time: int = configs.getint(
                "SECURITY", "TOKEN_EXPIRATION_TIME"
            )
            self.datatime_format: str = configs.get("SECURITY", "DATETIME_FORMAT")
            self.opa_url: str = configs.get("SECURITY", "OPA_URL")
            self.opa_public_key: str = configs.get("SECURITY", "OPA_PUBLIC_KEY")
