from fastapi import WebSocket, status, WebSocketException
from fastapi.security import OAuth2PasswordBearer


class AuthWebsocketBearer(OAuth2PasswordBearer):
    async def __call__(self, websocket: WebSocket):
        """
        Get token from header
        :param websocket:
        :return:
        """
        auth_header = websocket.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return
        scheme, token = auth_header.split()
        if scheme.lower() != "bearer":
            raise WebSocketException(
                code=status.WS_1008_POLICY_VIOLATION,
                reason="Invalid authentication credentials",
            )
        return token
