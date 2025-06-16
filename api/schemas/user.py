from enum import Enum
from typing import List, Optional

from sqlmodel import SQLModel, Field

from .common import RetrieveModelsQuery, RetrieveModelQuery
from api.models.accounts import UserGroup


class UserColumn(str, Enum):
    id: str = 'id'
    name: str = 'name'
    email: str = 'email'
    group: str = 'group'


class RetrieveUsersQuery(RetrieveModelsQuery):
    columns: Optional[List[UserColumn]] = Field(default=None)


class RetrieveUserQuery(RetrieveModelQuery):
    columns: Optional[List[UserColumn]] = Field(default=None)


class BaseUser(SQLModel):
    name: str = Field(index=True)
    email: str = Field()
    group: Optional[UserGroup] = Field(default=None)


class CreatedUserBody(BaseUser):
    pass


class RetrievedUser(BaseUser):
    id: int


class UpdatedUserBody(BaseUser):
    name: Optional[str] = Field(default=None, index=True)
    email: Optional[str] = Field(default=None)
