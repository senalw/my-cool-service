from configparser import ConfigParser
from typing import Any

from settings import ROOT_DIR
from src.config.env_interpolation import EnvInterpolation


class Config:
    @classmethod
    def get_instance(cls: Any) -> Any:
        if not getattr(cls, "_instance", None):
            cls._instance = cls()
        return cls._instance

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

    class DatabaseConfig:
        def __init__(self, configs: ConfigParser) -> None:
            self.db_url: str = configs.get("Database", "DB_URL")

    class ProjectConfig:
        def __init__(self, configs: ConfigParser) -> None:
            self.name: str = configs.get("Project", "NAME")
            self.api: str = configs.get("Project", "API")
            self.version: str = configs.get("Project", "VERSION")
