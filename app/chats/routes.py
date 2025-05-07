from fastapi import APIRouter, Depends, status

from app.chats.schemas import ChatCreate, SingleChat
from app.chats.services import ChatService
from app.users.auth import get_token_payload
from app.users.schemas import TokenPayload

router = APIRouter()


@router.get("/chats")
async def get_chats(payload: TokenPayload = Depends(get_token_payload), chat_service: ChatService = Depends()):
    return await chat_service.get_chats(payload)


@router.get("/chats/{chat_id}", response_model=SingleChat)
async def get_chat(chat_id: int, payload: TokenPayload = Depends(get_token_payload),
                   chat_service: ChatService = Depends()):
    return await chat_service.get_chat_by_id(chat_id, payload)


@router.post("/chats", status_code=status.HTTP_201_CREATED)
async def create_chat(chat_data: ChatCreate, payload: TokenPayload = Depends(get_token_payload),
                      chat_service: ChatService = Depends()):
    return await chat_service.create_chat(chat_data, payload)


@router.put("/chats/{chat_id}", status_code=status.HTTP_200_OK)
async def update_chat(chat_data: ChatCreate, chat_id: int, payload: TokenPayload = Depends(get_token_payload),
                      chat_service: ChatService = Depends()):
    return await chat_service.update_chat(chat_id, chat_data, payload)


@router.delete("/chats/{chat_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_chat(chat_id: int, payload: TokenPayload = Depends(get_token_payload),
                      chat_service: ChatService = Depends()):
    return await chat_service.delete_chat(chat_id, payload)
