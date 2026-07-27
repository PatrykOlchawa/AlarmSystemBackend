from fastapi import WebSocket
from collections import defaultdict
from collections.abc import Iterable
class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[int, set[WebSocket]]= defaultdict(set)

    async def connect(
        self,
        user_id: int,
        websocket: WebSocket,
    ) -> None:
        await websocket.accept()
        self.active_connections[user_id].add(websocket)

    def disconnect(
        self,
        user_id: int,
        websocket: WebSocket,
    ) -> None:
        connections = self.active_connections.get(user_id)

        if connections is None:
            return

        connections.discard(websocket)

        if not connections:
            del self.active_connections[user_id]

    async def send_to_user(
        self,
        user_id: int,
        message: dict,
    ) -> None:
        connections = self.active_connections.get(user_id)

        if not connections:
            return

        self.disconnected : list[WebSocket] = []

        for websocket in connections:
            try:
                await websocket.send_json(message)
            except Exception:
                self.disconnected.append(websocket)

        for websocket in self.disconnected:
            self.disconnect(user_id, websocket)
        
    def is_connected(
        self,
        user_id: int,
    ) -> bool:
        if self.active_connections.get(user_id) is None:
            return False
        return True

    async def broadcast(
        self,
        user_ids: Iterable[int],
        message: dict
    ) -> None:
        for user_id in user_ids:
            await self.send_to_user(user_id, message)
connection_manager = ConnectionManager() 