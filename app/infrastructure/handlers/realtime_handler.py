from fastapi import APIRouter, WebSocket, WebSocketDisconnect, status, Query
from typing import List

from app.infrastructure.schemas.message_schema import MessageFinalResponse

from fastapi.encoders import jsonable_encoder

realtime_router = APIRouter()

# Lista de clientes WebSocket conectados
connected_clients: List[WebSocket] = []

# Lista de tokens válidos (puedes cargar desde config o base de datos)
VALID_TOKENS = {"secret", "token"}

@realtime_router.websocket("/ws/messages")
async def websocket_endpoint(websocket: WebSocket, token: str = Query(...)):
    """
    Endpoint WebSocket para recibir mensajes en tiempo real.
    Permite a los clientes conectarse y recibir notificaciones automáticas
    cuando se crea un nuevo mensaje.
    """
        # Validar el token
    if token not in VALID_TOKENS:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return
    
    await websocket.accept()
    connected_clients.append(websocket)

    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        connected_clients.remove(websocket)

async def broadcast_message(message: MessageFinalResponse):
    """
    Envía un mensaje a todos los clientes WebSocket conectados.

    Args:
        message (MessageFinalResponse): Mensaje a enviar a los clientes conectados.
    """
    for client in connected_clients:
        try:
            json_message = jsonable_encoder(message)
            await client.send_json(json_message)
        except Exception:
            connected_clients.remove(client)