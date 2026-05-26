from pydantic import BaseModel
from typing import Optional


class TicketCreate(BaseModel):
    text: str


class TicketRead(BaseModel):
    id: int
    text: str
    category: Optional[str] = None

    class Config:
        orm_mode = True



class UserCreate(BaseModel):
    username: str
    password: str


class UserRead(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
