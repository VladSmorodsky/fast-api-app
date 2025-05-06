from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from app.background_tasks import send_register_email
from app.users.auth import create_access_token
from app.users.crud import create_user, get_user_by_creds
from app.users.schemas import UserCreate, UserResponse, ResponseUserCreate, UserLogin, ResponseUserLogin
from app.utils import get_db

router = APIRouter()


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user_body: UserCreate, background_task: BackgroundTasks,
                        db: AsyncSession = Depends(get_db)) -> ResponseUserCreate:
    try:
        user = await create_user(db, user_body)
        background_task.add_task(send_register_email, user.email)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    if not user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User with email or username already exists.",
        )

    access_token = create_access_token(user)

    user_data = UserResponse(username=user.username, email=user.email)
    return ResponseUserCreate(message='User created', user=user_data, token=access_token)


@router.post("/login")
async def login(user_data: UserLogin, db: AsyncSession = Depends(get_db)):
    user = await get_user_by_creds(db, str(user_data.email), user_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    access_token = create_access_token(user=user)
    user_data = UserResponse(username=user.username, email=user.email)
    return ResponseUserLogin(user=user_data, token=access_token)
