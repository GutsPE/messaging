from pydantic import BaseModel
from datetime import datetime
from typing import Literal

class MessageRequest(BaseModel):
    """
    Esquema de entrada para creación o envío de un mensaje.
    """
    message_id: str
    session_id: str
    content: str
    timestamp: datetime
    sender: Literal["user", "system"]


class MessageResponse(MessageRequest):
    """
    Esquema de respuesta de un mensaje completo con campos adicionales.
    """
    id: int
    length: int
    word_count: int

    class Config:
        orm_mode = True

class MetadataResponse(BaseModel):
    """
    Metadatos adicionales procesados a partir del contenido del mensaje.
    """
    word_count: int
    character_count: int
    processed_at: datetime

class MessageCustomResponse(BaseModel):
    """
    Respuesta que combina datos del mensaje original con los metadatos generados.
    """
    message_id: str
    session_id: str
    content: str
    timestamp: datetime
    sender: Literal["user", "system"]
    metadata: MetadataResponse

class MessageFinalResponse(BaseModel):
    """
    Respuesta final completa que encapsula el estado y el contenido enriquecido del mensaje.
    """
    status: str
    data: MessageCustomResponse