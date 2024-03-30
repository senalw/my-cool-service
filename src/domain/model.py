from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Association table for the many-to-many relationship between users and roles
user_role_association = Table(
    "user_role_association",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("user.user_id")),
    Column("role_id", Integer, ForeignKey("role.role_id")),
)


class UserModel(Base):
    __tablename__ = "user"

    user_id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String(100), nullable=False)  # Hashed password
    email = Column(String, unique=True, nullable=False)

    roles = relationship("RoleModel", secondary=user_role_association, backref="users")


class RoleModel(Base):
    __tablename__ = "role"

    role_id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
