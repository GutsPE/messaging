from sqlalchemy import Column, Integer, String, DateTime
from app.infrastructure.connection.sync_db.database import database_conn


class MessageModel(database_conn.base):
    """
    Modelo ORM que representa la tabla 'messages' en la base de datos.
    Utiliza SQLAlchemy como ORM.

    Atributos:
        id (int): Clave primaria autoincremental del mensaje.
        message_id (str): Identificador único del mensaje (UUID u otro formato).
        session_id (str): Identificador de la sesión a la que pertenece el mensaje.
        content (str): Contenido textual del mensaje.
        timestamp (datetime): Fecha y hora en que se creó el mensaje.
        sender (str): Remitente del mensaje (ej. 'user' o 'system').
        length (int): Longitud del contenido del mensaje (cantidad de caracteres).
        word_count (int): Número de palabras en el contenido del mensaje.
    """
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    message_id = Column(String, unique=True, nullable=False)
    session_id = Column(String, index=True, nullable=False)
    content = Column(String, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    sender = Column(String, nullable=False)
    length = Column(Integer)
    word_count = Column(Integer)