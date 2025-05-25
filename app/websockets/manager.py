from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, set[WebSocket]] = {}

    async def connect(self, room: str, websocket: WebSocket):
        await websocket.accept()
        room_conns = self.active_connections.setdefault(room, set())
        room_conns.add(websocket)

    def disconnect(self, room: str, websocket: WebSocket):
        conns = self.active_connections.get(room)
        if conns:
            conns.discard(websocket)
            if not conns:
                # clean up empty room
                del self.active_connections[room]

    async def broadcast(self, room: str, username: str, message: str, exclude: WebSocket = None):
        for connection in self.active_connections.get(room, []):
            await connection.send_json({
                'username': username,
                'message': message,
            })
