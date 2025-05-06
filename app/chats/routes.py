from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.chats.crud import get_user_chats, create_user_chat, get_chat_by_id
from app.chats.schemas import ChatCreate, SingleChat
from app.users.auth import get_token_payload
from app.users.crud import get_users_by_id
from app.users.schemas import TokenPayload
from app.utils import get_db

router = APIRouter()


@router.get("/chats")
async def get_chats(payload: TokenPayload = Depends(get_token_payload), db: AsyncSession = Depends(get_db)):
    return await get_user_chats(db, payload)

@router.get("/chats/{chat_id}", response_model=SingleChat)
async def get_chat(chat_id: int, db: AsyncSession = Depends(get_db)):
    chat = await get_chat_by_id(db, chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    return chat

@router.post("/chats", status_code=status.HTTP_201_CREATED)
async def create_chat(chat_data: ChatCreate, db: AsyncSession = Depends(get_db)):
    users = await get_users_by_id(db, chat_data.user_ids)
    if not users:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No users found")
    await create_user_chat(db, chat_data.name, users)
    return
