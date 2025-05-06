from typing import Sequence

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from email_validator import (
    validate_email,
    EmailNotValidError,
)

from app.models import User
from app.users.schemas import UserCreate
from app.users.auth import hash_password, verify_password


async def create_user(db: AsyncSession, user_body: UserCreate) -> User | None:
    hashed_password = hash_password(user_body.password)
    user = User(username=user_body.username, email=str(user_body.email), password=hashed_password)
    try:
        db.add(user)
        await db.commit()
        await db.refresh(user)
    except IntegrityError:
        await db.rollback()
        return None
    return user


async def get_user_by_creds(db: AsyncSession, email: str, password: str) -> User | None:
    """
    Get user by email and password
    :param db:
    :param email:
    :param password:
    :return:
    """
    try:
        validate_email(email)
    except EmailNotValidError:
        return None
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    if not user or not verify_password(password, user.password):
        return None
    return user


async def get_users_by_id(db: AsyncSession, user_ids: list[int]) -> Sequence[User]:
    """
    Get user list by list of ids
    :param db:
    :param user_ids:
    :return:
    """
    result = await db.execute(select(User).where(User.id.in_(user_ids)))
    users = result.scalars().all()
    return users


async def get_user_by_id(db: AsyncSession, user_id: int) -> User | None:
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    return user
