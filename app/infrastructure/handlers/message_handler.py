from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi import Request

from app.application.services.search_messages_by_content import SearchMessagesByContent
from app.infrastructure.connection.sync_db.database import database_conn
from datetime import datetime, timezone

# Servicios de aplicación
from app.application.services.get_all_messages_by_session import GetAllMessagesBySession
from app.application.services.get_message import GetMessage
from app.application.services.create_message import CreateMessage
from app.application.services.get_all_messages import GetAllMessages

# Excepciones
from app.domain.exceptions.message_exceptions import MessageNotFoundException

# Repositorio
from app.infrastructure.repositories.sql_message_repository import SQLMessageRepository

# Esquemas Pydantic
from app.infrastructure.schemas.message_schema import (
    MessageRequest, 
    MessageResponse, 
    MessageFinalResponse, 
    MessageCustomResponse, 
    MetadataResponse
)

from app.infrastructure.handlers.realtime_handler import broadcast_message
from app.infrastructure.security.limiting import limiter

message_router = APIRouter(
    prefix="/messages",
    tags=["messages"],
    responses={404: {"description": "Not found"}}
)

# ----------------------------
# GET /messages
# ----------------------------
@message_router.get("/", response_model=list[MessageResponse])
def get_Messages(db: Session = Depends(database_conn.get_db)):
    """
    Recupera todos los mensajes almacenados en la base de datos.

    Returns:
        Lista de mensajes en formato MessageResponse.
    """
    repository = SQLMessageRepository(db)
    use_case = GetAllMessages(repository)
    return [message.to_dict() for message in use_case.execute()]

# ----------------------------
# POST /messages
# ----------------------------
@message_router.post("/", response_model=MessageFinalResponse)
async def create_message(message: MessageRequest, db: Session = Depends(database_conn.get_db)):
    """
    Crea un nuevo mensaje.

    Args:
        message: Objeto que contiene los datos del mensaje.
    
    Returns:
        Objeto con estado de éxito y los datos del mensaje creado, incluyendo metadatos como longitud y cantidad de palabras.
    """
    repository = SQLMessageRepository(db)
    use_case = CreateMessage(repository)
    message_db = use_case.execute(message.message_id, message.session_id, message.content, message.timestamp, message.sender)
    response = MessageFinalResponse(
        status="success",
        data=MessageCustomResponse(
            message_id=message_db.message_id,
            session_id=message_db.session_id,
            content=message_db.content,
            timestamp=message_db.timestamp,
            sender=message_db.sender,
            metadata=MetadataResponse(
                word_count=message_db.word_count,
                character_count=message_db.length,
                processed_at=datetime.now(timezone.utc)
            )
        )
    )
    print("Enviando a WebSocket:", response.json())
    await broadcast_message(response)  # Notifica a los WebSocket
    
    return response

@message_router.get("/search", response_model=list[MessageResponse])
@limiter.limit("5/minute")
def search_messages(
    request: Request,
    query: str,
    limit: int = 10,
    offset: int = 0,
    db: Session = Depends(database_conn.get_db)
):
    """
    Busca mensajes por contenido usando una palabra clave.

    Args:
        query: Palabra clave a buscar dentro del contenido del mensaje.
        limit: Número máximo de resultados.
        offset: Offset para paginación.

    Returns:
        Lista de mensajes que coincidan con el contenido.
    """
    repository = SQLMessageRepository(db)
    use_case = SearchMessagesByContent(repository)
    return [message.to_dict() for message in use_case.execute(query=query, limit=limit, offset=offset)]

# ----------------------------
# GET /messages/{message_id}
# ----------------------------
@message_router.get("/{message_id}", response_model=MessageResponse)
def get_message(message_id: str, db: Session = Depends(database_conn.get_db)):
    """
    Recupera un mensaje por su ID.

    Args:
        message_id: ID único del mensaje.
    
    Returns:
        El mensaje si se encuentra. Lanza 404 si no existe.
    """
    repository = SQLMessageRepository(db)
    use_case = GetMessage(repository)
    try:
        message = use_case.execute(message_id)
        return message.to_dict()
    except MessageNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    
# ----------------------------
# GET /messages/sessions/{session_id}
# ----------------------------
@message_router.get("/sessions/{session_id}", response_model=list[MessageResponse])
def get_messages_by_session(
    session_id: str,
    limit: int = 10,
    offset: int = 0,
    sender: str | None = None,
    db: Session = Depends(database_conn.get_db)
):
    """
    Recupera todos los mensajes de una sesión dada.

    Args:
        session_id: ID de la sesión a filtrar.
        limit: Límite de resultados (paginación).
        offset: Offset de resultados (paginación).
        sender: Filtro opcional por remitente ('user' o 'system').

    Returns:
        Lista de mensajes en la sesión, posiblemente filtrados y paginados.
    """
    repository = SQLMessageRepository(db)
    use_case = GetAllMessagesBySession(repository)
    messages = use_case.execute(session_id=session_id, limit=limit, offset=offset, sender=sender)
    return [message.to_dict() for message in messages]
