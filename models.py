from pydantic import BaseModel, EmailStr
from sqlmodel import Field, Relationship, SQLModel
from sqlalchemy import Integer, Column



# Shared properties
class UserBase(SQLModel):
    full_name: str = Field(default="noname", max_length=20, unique=True, index=True)
    port: int = Field(unique=True, index=True)


# Properties to receive via API on creation
class UserCreate(UserBase):
    pass



# Database model, database table inferred from class name
class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


# Properties to return via API
class UserPublic(UserBase):
    pass


# class UsersPublic(SQLModel):
#     data: list[UserPublic]
#     count: int
