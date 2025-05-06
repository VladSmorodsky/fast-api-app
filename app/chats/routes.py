from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.chats.crud import get_user_chats, create_user_chat, get_chat_by_id
from app.chats.schemas import ChatCreate, SingleChat
from app.users.auth import get_token_payload
from app.users.crud import get_users_by_id, get_user_by_id
from app.users.schemas import TokenPayload
from app.utils import get_db

router = APIRouter()


@router.get("/chats")
async def get_chats(payload: TokenPayload = Depends(get_token_payload), db: AsyncSession = Depends(get_db)):
    authenticated_user = await get_user_by_id(db, payload.id)
    if not authenticated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return await get_user_chats(db, payload)


@router.get("/chats/{chat_id}", response_model=SingleChat)
async def get_chat(chat_id: int, db: AsyncSession = Depends(get_db),
                   payload: TokenPayload = Depends(get_token_payload)):
    authenticated_user = await get_user_by_id(db, payload.id)
    if not authenticated_user:
        raise HTTPException(status_code=404, detail="User not found")
    chat = await get_chat_by_id(db, chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    return chat


@router.post("/chats", status_code=status.HTTP_201_CREATED)
async def create_chat(chat_data: ChatCreate, db: AsyncSession = Depends(get_db),
                      payload: TokenPayload = Depends(get_token_payload)):
    authenticated_user = await get_user_by_id(db, payload.id)
    if not authenticated_user:
        raise HTTPException(status_code=404, detail="User not found")
    users = await get_users_by_id(db, chat_data.user_ids)
    if not users:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No users found")
    await create_user_chat(db, chat_data.name, users)
    return


@router.put("/chats/{chat_id}", status_code=status.HTTP_200_OK)
async def update_chat(chat_data: ChatCreate, chat_id: int, db: AsyncSession = Depends(get_db),
                      payload: TokenPayload = Depends(get_token_payload)):
    authenticated_user = await get_user_by_id(db, payload.id)
    if not authenticated_user:
        raise HTTPException(status_code=404, detail="User not found")
    chat = await get_chat_by_id(db, chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    users = await get_users_by_id(db, chat_data.user_ids)
    if not users:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No users found")
    chat.users = users
    chat.name = chat_data.name
    db.add(chat)
    await db.commit()
    await db.refresh(chat)
    return chat


@router.delete("/chats/{chat_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_chat(chat_id: int, db: AsyncSession = Depends(get_db),
                      payload: TokenPayload = Depends(get_token_payload)):
    authenticated_user = await get_user_by_id(db, payload.id)
    if not authenticated_user:
        raise HTTPException(status_code=404, detail="User not found")
    chat = await get_chat_by_id(db, chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    await db.delete(chat)
    await db.commit()
    return
