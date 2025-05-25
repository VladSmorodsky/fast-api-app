from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models import Chat, User, user_chat
from app.users.schemas import TokenPayload


async def get_user_chats(db: AsyncSession, payload: TokenPayload):
    """
    Get all chats where user exists
    :param db:
    :param payload:
    :return:
    """
    result = await db.execute(select(Chat).join(user_chat).join(User).where(User.id == payload.id))
    user_chats = result.scalars().all()
    return user_chats


async def get_chat_by_id(db: AsyncSession, chat_id: int, user_id: int):
    """
    Get chat by chat id
    :param db:
    :param chat_id:
    :param user_id:
    :return:
    """
    result = await db.execute(
        select(Chat)
        .options(selectinload(Chat.users))
        .where(Chat.id == int(chat_id))
        .where(Chat.users.any(User.id == user_id))
    )
    chat = result.scalars().first()
    return chat


async def create_user_chat(db: AsyncSession, chat_name: str, users: Sequence[User]):
    chat = Chat(name=chat_name)
    chat.users = users
    db.add(chat)
    await db.commit()
    await db.refresh(chat)
