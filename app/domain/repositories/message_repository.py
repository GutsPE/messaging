from abc import ABC, abstractmethod
from typing import List
from app.domain.entities.message import Message

class MessageRepository(ABC):
    """
    Interfaz abstracta para definir los métodos de acceso y manipulación de entidades Message 
    en una fuente de datos (por ejemplo, base de datos, memoria, etc.).
    """
    
    @abstractmethod
    def get_all(self) -> List[Message]:
        """
        Recupera todos los mensajes disponibles.

        Returns:
            List[Message]: Lista de todos los mensajes.
        """
        pass

    @abstractmethod
    def get_by_id(self, message_id: str) -> Message:
        """
        Recupera un mensaje específico por su identificador.

        Args:
            message_id (str): Identificador único del mensaje.

        Returns:
            Message: Objeto mensaje correspondiente.
        """
        pass

    @abstractmethod
    def save(self, message: Message) -> Message:
        """
        Guarda un nuevo mensaje en el repositorio.

        Args:
            message (Message): Objeto mensaje a guardar.

        Returns:
            Message: Mensaje guardado con posibles campos actualizados (e.g., ID generado).
        """
        pass
    
    @abstractmethod
    def get_by_session(
        self, 
        session_id: str, 
        limit: int = 10, 
        offset: int = 0, 
        sender: str | None = None
    ) -> Message:
        """
        Recupera una lista de mensajes asociados a una sesión, con soporte de paginación y filtrado por remitente.

        Args:
            session_id (str): ID de la sesión.
            limit (int): Número máximo de mensajes a retornar (paginación).
            offset (int): Número de mensajes a omitir desde el inicio (paginación).
            sender (str | None): Remitente a filtrar (por ejemplo, 'user' o 'system').

        Returns:
            List[Message]: Lista de mensajes filtrados por sesión y remitente.
        """
        pass
    
    @abstractmethod
    def search_by_content(
        self, 
        query: str, 
        limit: int = 10, 
        offset: int = 0
    ) -> Message:
        """
        Recupera una lista de mensajes asociados a una sesión, con soporte de paginación y filtrado por remitente.

        Args:
            session_id (str): ID de la sesión.
            limit (int): Número máximo de mensajes a retornar (paginación).
            offset (int): Número de mensajes a omitir desde el inicio (paginación).
            sender (str | None): Remitente a filtrar (por ejemplo, 'user' o 'system').

        Returns:
            List[Message]: Lista de mensajes filtrados por sesión y remitente.
        """
        pass