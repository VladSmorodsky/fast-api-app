from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.chats.crud import get_user_chats, get_chat_by_id, create_user_chat
from app.chats.schemas import ChatCreate
from app.users.crud import is_auth_user, get_users_by_id
from app.users.schemas import TokenPayload
from app.utils import get_db


class ChatService:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def get_chats(self, payload: TokenPayload) -> None:
        await is_auth_user(self.db, payload)
        return await get_user_chats(self.db, payload)

    async def get_chat_by_id(self, chat_id: int, payload: TokenPayload):
        await is_auth_user(self.db, payload)
        chat = await get_chat_by_id(self.db, chat_id, payload.id)
        if not chat:
            raise HTTPException(status_code=404, detail="Chat not found")
        return chat

    async def create_chat(self, chat_data: ChatCreate, payload: TokenPayload):
        await is_auth_user(self.db, payload)
        users = await get_users_by_id(self.db, chat_data.user_ids)
        if not users:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No users found")
        await create_user_chat(self.db, chat_data.name, users)
        return

    async def update_chat(self, chat_id: int, chat_data: ChatCreate, payload: TokenPayload):
        await is_auth_user(self.db, payload)
        chat = await get_chat_by_id(self.db, chat_id, payload.id)
        if not chat:
            raise HTTPException(status_code=404, detail="Chat not found")
        users = await get_users_by_id(self.db, chat_data.user_ids)
        if not users:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No users found")
        chat.users = users
        chat.name = chat_data.name
        self.db.add(chat)
        await self.db.commit()
        await self.db.refresh(chat)
        return chat

    async def delete_chat(self, chat_id: int, payload: TokenPayload):
        await is_auth_user(self.db, payload)
        chat = await get_chat_by_id(self.db, chat_id, payload.id)
        if not chat:
            raise HTTPException(status_code=404, detail="Chat not found")
        await self.db.delete(chat)
        await self.db.commit()
        return
