from fastapi import WebSocket
from collections import defaultdict
import json

class ConnectionManager:
    def __init__(self):
        self.active_connections = defaultdict(list)

    async def connect(self,websocket: WebSocket, user_id: int):
        await websocket.accept()
        self.active_connections[user_id].append(websocket)

    def disconnect(self,websocket: WebSocket, user_id: int):
        self.active_connections[user_id].remove(websocket)

    async def send_personal_message(
        self,
        user_id: int,
        message: dict
    ):
        connections = self.active_connections.get(user_id, [])

        for connection in connections:
            await connection.send_text(
                json.dumps(message)
            )

manager = ConnectionManager()