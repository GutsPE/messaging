from app.domain.repositories.message_repository import MessageRepository
from app.domain.entities.message import Message
from datetime import datetime

class CreateMessage:
    """
    Caso de uso para crear y guardar un nuevo mensaje.
    Esta clase representa la lógica de aplicación para procesar un mensaje entrante
    y almacenarlo en el repositorio correspondiente.
    """
    def __init__(self, repository: MessageRepository):
        """
        Constructor de la clase.

        Args:
            repository (MessageRepository): Repositorio donde se guardarán los mensajes.
        """
        self.repository = repository

    def execute(
        self, 
        message_id: str, 
        session_id: str, 
        content: str, 
        timestamp: datetime, 
        sender: str
    ):
        """
        Ejecuta la lógica para crear y guardar un nuevo mensaje.

        Args:
            message_id (str): Identificador único del mensaje.
            session_id (str): Identificador de sesión al que pertenece el mensaje.
            content (str): Contenido del mensaje.
            timestamp (datetime): Fecha y hora en que fue enviado el mensaje.
            sender (str): Remitente del mensaje, puede ser "user" o "system".

        Returns:
            Message: Objeto del dominio representando el mensaje guardado.
        """
        # Se crea la entidad de dominio `Message` con metadatos calculados
        message = Message(
            message_id=message_id, 
            session_id=session_id, 
            content=content, 
            timestamp=timestamp, 
            sender=sender, 
            length=len(content), 
            word_count=len(content.split())
        )
        # Se guarda el mensaje usando el repositorio
        return self.repository.save(message)