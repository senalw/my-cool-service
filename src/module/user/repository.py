from abc import ABC, abstractmethod
from typing import List, Optional

from src.core.database.postgres_client import PostgresClient
from src.domain import UserModel
from src.domain.user_dto import UserDomain
from src.module.user.mapper import UserMapper


class UserRepository(ABC):
    @abstractmethod
    def add_user(self, user: UserModel) -> UserDomain:
        raise NotImplementedError

    @abstractmethod
    def get_user_by_id(self, user_name: str) -> Optional[UserDomain]:
        raise NotImplementedError

    @abstractmethod
    def get_users(self) -> List[UserDomain]:
        raise NotImplementedError


class UserRepositoryImpl(UserRepository):
    def __init__(self, db: PostgresClient) -> None:
        self.db: PostgresClient = db

    def add_user(self, user: UserModel) -> UserDomain:
        with self.db.get_session() as session:
            session.add(user)
            return UserMapper.to_domain(user)

    def get_user_by_id(self, user_name: str) -> Optional[UserDomain]:
        with self.db.get_session() as session:
            user: Optional[UserModel] = (
                session.query(UserModel).filter_by(username=user_name).first()
            )
            if user:
                return UserMapper.to_domain(user)

    def get_users(self) -> List[UserDomain]:
        with self.db.get_session() as session:
            return [
                UserMapper.to_domain(user) for user in session.query(UserModel).all()
            ]
