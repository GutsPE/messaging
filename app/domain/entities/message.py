from datetime import datetime
from typing import Optional

class Message:
    """
    Entidad de dominio que representa un mensaje dentro del sistema.
    """
    
    def __init__(
        self, 
        message_id: str, 
        session_id: str, 
        content: str, 
        timestamp: datetime, 
        sender: str, 
        length: int, 
        word_count: int,
        id: Optional[int] = None
    ):
        """
        Inicializa una nueva instancia de Message.

        Args:
            message_id (str): Identificador único del mensaje.
            session_id (str): Identificador de la sesión a la que pertenece el mensaje.
            content (str): Contenido textual del mensaje.
            timestamp (datetime): Fecha y hora en que se envió el mensaje.
            sender (str): Remitente del mensaje ('user' o 'system').
            length (int): Longitud del contenido en caracteres.
            word_count (int): Número de palabras en el contenido.
            id (Optional[int], optional): ID interno en base de datos (autogenerado). Por defecto, None.
        """
        self.id = id
        self.message_id = message_id
        self.session_id = session_id
        self.content = content
        self.timestamp = timestamp
        self.sender = sender
        self.length = length
        self.word_count = word_count

    def to_dict(self):
        """
        Convierte la entidad `Message` a un diccionario, útil para serialización o respuestas API.

        Returns:
            dict: Representación del mensaje en formato clave-valor.
        """
        return {
            "id": self.id,
            "message_id": self.message_id,
            "session_id": self.session_id,
            "content": self.content,
            "timestamp": self.timestamp,
            "sender": self.sender,
            "length": self.length,
            "word_count": self.word_count
        }