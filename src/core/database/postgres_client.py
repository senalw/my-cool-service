import logging
from contextlib import contextmanager

from fastapi import status
from sqlalchemy import create_engine, Engine, text
from sqlalchemy.exc import DataError, IntegrityError, OperationalError, ProgrammingError
from sqlalchemy.orm import Session, sessionmaker
from src.config.config import Config
from src.core.exception import (
    AlreadyExistsError,
    DatabaseConnectionError,
    InvalidArgumentError,
    MyCoolServiceError,
)
from src.domain.model import Base


class PostgresClient:
    def __init__(self, configs: Config) -> None:
        self.db_engine: Engine = create_engine(configs.db_configs.db_url)

    @contextmanager
    def get_session(self) -> Session:
        session = None
        try:
            # "auto flush" should be turned off for merging objects in a same session.
            sm = sessionmaker(bind=self.db_engine, autoflush=False)
            session = sm()
            yield session
            session.commit()
        except Exception as e:
            if session:
                session.rollback()
            self._handle_db_errors(e)
        finally:
            if session:
                session.flush()
                session.close()

    def drop_tables(self) -> None:
        Base.metadata.drop_all(self.db_engine)

    def create_tables(self) -> None:
        Base.metadata.create_all(self.db_engine)

    def insert_sample_data(self) -> None:
        for table in ["user"]:
            with open(f"resources/sample_data/{table}.sql", "r") as sql_file:
                with self.get_session() as session:
                    for statement in sql_file:
                        session.execute(text(statement))

    @staticmethod
    def _handle_db_errors(throwable: Exception) -> None:
        logging.exception(throwable)

        if isinstance(throwable, MyCoolServiceError):
            raise throwable
        elif isinstance(
            throwable,
            DataError,
        ):  # passing None/Incorrect parameter for mandatory parameter
            raise InvalidArgumentError("Invalid argument")
        elif isinstance(throwable, AttributeError):
            raise InvalidArgumentError(f"Invalid attribute: [{throwable.name}]")
        elif isinstance(
            throwable, (OperationalError, ProgrammingError)
        ):  # Programming error occurs when table not found
            raise DatabaseConnectionError("Unable to connect to the database")
        elif isinstance(throwable, IntegrityError):  # db constraint error
            raise AlreadyExistsError("Unique key or Not null violation")
        else:
            raise MyCoolServiceError(
                "Unknown Error", status.HTTP_500_INTERNAL_SERVER_ERROR
            )
