from sqlalchemy.orm import Session
from app.domain.repositories.message_repository import MessageRepository
from app.domain.entities.message import Message
from app.infrastructure.repositories.models.message_model import MessageModel


class SQLMessageRepository(MessageRepository):
    """
    Implementación concreta del repositorio de mensajes que utiliza SQLAlchemy
    para interactuar con una base de datos relacional.
    """
    
    def __init__(self, session: Session):
        """
        Inicializa el repositorio con una sesión de base de datos.
        
        Args:
            session (Session): Sesión SQLAlchemy activa.
        """
        self.session = session

    def get_all(self):
        """
        Recupera todos los mensajes almacenados en la base de datos.

        Returns:
            List[Message]: Lista de entidades de dominio Message.
        """
        return [
            Message(
                id=message.id, 
                message_id=message.message_id, 
                session_id=message.session_id, 
                content=message.content, 
                timestamp= message.timestamp, 
                sender=message.sender, 
                length=message.length, 
                word_count=message.word_count
            ) 
            for message in self.session.query(MessageModel).all()]

    def get_by_id(self, message_id: int):
        """
        Recupera un mensaje específico por su message_id.

        Args:
            message_id (str): Identificador único del mensaje.

        Returns:
            Message | None: Entidad Message o None si no se encuentra.
        """
        message = self.session.query(MessageModel).filter(MessageModel.message_id == message_id).first()
        if not message:
            return None
        return Message(
            id=message.id, 
            message_id=message.message_id, 
            session_id=message.session_id, 
            content=message.content, 
            timestamp= message.timestamp, 
            sender=message.sender, 
            length=message.length, 
            word_count=message.word_count
        )

    def save(self, message: Message):
        """
        Persiste un nuevo mensaje en la base de datos.

        Args:
            message (Message): Entidad Message del dominio.

        Returns:
            Message: Entidad Message persistida (con ID generado).
        """
        db_message = MessageModel(
            message_id=message.message_id, 
            session_id=message.session_id, 
            content=message.content, 
            timestamp= message.timestamp, 
            sender=message.sender, 
            length=message.length, 
            word_count=message.word_count
        )
        self.session.add(db_message)
        self.session.commit()
        return Message(
            id=db_message.id, 
            message_id=db_message.message_id, 
            session_id=db_message.session_id, 
            content=db_message.content, 
            timestamp= db_message.timestamp, 
            sender=db_message.sender, 
            length=db_message.length, 
            word_count=db_message.word_count
        )
        
    def get_by_session(
        self, 
        session_id: str, 
        limit: int = 10, 
        offset: int = 0, 
        sender: str | None = None
    ):
        """
        Recupera mensajes por ID de sesión, con soporte para paginación y filtrado por remitente.

        Args:
            session_id (str): Identificador de la sesión.
            limit (int): Número máximo de resultados a devolver.
            offset (int): Número de resultados a omitir desde el inicio.
            sender (str | None): Opcional. Filtrar por remitente ("user" o "system").

        Returns:
            List[Message]: Lista de mensajes que coinciden con los filtros.
        """
        query = self.session.query(MessageModel).filter(MessageModel.session_id == session_id)

        if sender:
            query = query.filter(MessageModel.sender == sender)

        query = query.offset(offset).limit(limit)

        messages = query.all()

        return [
            Message(
                id=message.id,
                message_id=message.message_id,
                session_id=message.session_id,
                content=message.content,
                timestamp=message.timestamp,
                sender=message.sender,
                length=message.length,
                word_count=message.word_count
            )
            for message in messages
        ]
        
    def search_by_content(
        self, 
        query: str, 
        limit: int = 10, 
        offset: int = 0
    ) -> list[Message]:
        return [
            Message(
                id=message.id, 
                message_id=message.message_id, 
                session_id=message.session_id, 
                content=message.content, 
                timestamp= message.timestamp, 
                sender=message.sender, 
                length=message.length, 
                word_count=message.word_count
            ) 
            for message in self.session.query(MessageModel) 
            .filter(MessageModel.content.ilike(f"%{query}%"))
            .offset(offset)
            .limit(limit)
            .all()
        ]
