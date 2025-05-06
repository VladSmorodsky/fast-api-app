from contextlib import asynccontextmanager

from fastapi import FastAPI
from app.database import engine, Base

from app.users.routes import router as users_router
from app.chats.routes import router as chats_router
from app.websockets.routes import router as websockets_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(users_router)
app.include_router(chats_router)
app.include_router(websockets_router)
