from datetime import datetime, timedelta

from passlib.context import CryptContext
from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import (
    OAuth2PasswordBearer,
)

from app.models import User
from app.settings import HASH_ALGORITHM, SECRET_KEY, ACCESS_TOKEN_TTL
from app.users.schemas import TokenPayload

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login", scheme_name='JWT')


def get_token_payload(token: str = Depends(oauth2_scheme)) -> TokenPayload:
    """
    Get token payload from header
    :param token:
    :return:
    """
    try:
        payload = decode_access_token(token)
    except JWTError as error:
        print("Authentication Error:", error)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return payload


def hash_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_context.verify(plain_password, hashed_password)


def create_access_token(user: User) -> str:
    data = {"sub": str(user.id)}
    return create_token(data)


def create_token(user_data: dict) -> str:
    to_encode = user_data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_TTL)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, HASH_ALGORITHM)


def decode_access_token(token: str) -> TokenPayload:
    payload = jwt.decode(token, SECRET_KEY, HASH_ALGORITHM)
    return TokenPayload(id=payload["sub"])
