import uuid
from datetime import datetime

from fastapi_users import schemas
from pydantic import UUID4, BaseModel


class UserRead(schemas.BaseUser[uuid.UUID]):
    pass


class UserCreate(schemas.BaseUserCreate):
    pass

class FileCreate(BaseModel):
    path: str

class FileRead(BaseModel):
    id: UUID4
    name: str
    created_at: datetime
    path: str
    size: int
    is_downloadable: bool

    class Config:
        orm_mode = True



# class UserRegister(BaseModel):
#    login: str
#    password: str


class FileReadList(FileRead):
    author: UUID4|None

    class Config:
        orm_mode = True
