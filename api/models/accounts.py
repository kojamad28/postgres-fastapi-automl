from typing import Optional

from sqlmodel import SQLModel, Field


class UserGroup(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, max_length=20)
    description: Optional[str] = Field(default=None)


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, max_length=20)
    email: str = Field()
    group: Optional[UserGroup] = Field(default=None)
