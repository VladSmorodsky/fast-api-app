from fastapi import APIRouter, WebSocket, WebSocketDisconnect, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.chats.crud import get_chat_by_id
from app.websockets.auth import AuthWebsocketBearer
from app.websockets.manager import ConnectionManager
from app.users.auth import get_token_payload
from app.users.crud import get_user_by_id
from app.utils import get_db

router = APIRouter()

websocket_auth = AuthWebsocketBearer(tokenUrl='/login')
manager = ConnectionManager()

ROOM_CHAT_PREFIX = 'room_'


@router.websocket("/ws/chat/{chat_id}")
async def ws_chat(websocket: WebSocket, chat_id: int, db: AsyncSession = Depends(get_db),
                  token: str = Depends(websocket_auth)):
    token_payload = get_token_payload(token)
    user = await get_user_by_id(db, token_payload.id)

    if user is None:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return
    chat = await get_chat_by_id(db, chat_id, token_payload.id)
    if chat is None:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return
    chat_users = [c for c in chat.users if user.username == c.username]
    if len(chat_users) == 0:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    room_name = f"{ROOM_CHAT_PREFIX}{chat.id}"
    await manager.connect(room_name, websocket)
    await manager.broadcast(
        room_name,
        user.username,
        f"{user.username} joined the chat",
        exclude=websocket,
    )
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(room_name, user.username, data)
    except WebSocketDisconnect:
        manager.disconnect(room_name, websocket)
        await manager.broadcast(room_name, user.username, f"Client {user.username} left the chat")
