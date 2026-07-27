from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.core.websocket.manager import connection_manager
from app.security.jwt_handler import jwt_handler
from app.core.exceptions import InvalidTokenException 

router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket
):
    token = websocket.query_params.get("token")

    if token is None:
        await websocket.close(code=1008)
        return

    try:
        user_id = jwt_handler.get_user_id(token=token)
    except InvalidTokenException:
        await websocket.close(code=1008)
        return

    await connection_manager.connect(user_id, websocket)

    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        connection_manager.disconnect(user_id, websocket)
