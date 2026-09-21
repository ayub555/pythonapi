from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    firstname: str
    lastname: str
    phoneno: str
    emailId: str
    username: str
    password: str
    createddate: Optional[datetime] = None
    lastlogin: Optional[datetime] = None


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    pass


class User(UserBase):
    userId: int
