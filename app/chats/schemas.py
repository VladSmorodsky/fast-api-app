from typing import List

from pydantic import BaseModel

from app.users.schemas import UserResponse


class ChatCreate(BaseModel):
    name: str
    user_ids: List[int]

class SingleChat(BaseModel):
    name: str
    users: List[UserResponse]
    class Config:
        orm_mode = True
