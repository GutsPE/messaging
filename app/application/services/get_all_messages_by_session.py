from app.domain.repositories.message_repository import MessageRepository

class GetAllMessagesBySession:
    """
    Caso de uso para obtener todos los mensajes de una sesión específica,
    con soporte para paginación y filtrado por remitente.
    """
    def __init__(self, repository: MessageRepository):
        """
        Inicializa la clase con un repositorio de mensajes.

        Args:
            repository (MessageRepository): Repositorio que provee acceso a los datos de mensajes.
        """
        self.repository = repository

    def execute(
        self, 
        session_id: str, 
        limit: int = 10, 
        offset: int = 0, 
        sender: str | None = None
    ):
        """
        Ejecuta la lógica para recuperar mensajes asociados a una sesión,
        aplicando paginación y filtrado opcional por remitente.

        Args:
            session_id (str): Identificador de la sesión cuyos mensajes se desean recuperar.
            limit (int, opcional): Número máximo de mensajes a retornar. Valor por defecto: 10.
            offset (int, opcional): Número de mensajes a omitir desde el inicio. Valor por defecto: 0.
            sender (str | None, opcional): Si se especifica, filtra los mensajes por el remitente ("user" o "system").

        Returns:
            list[Message]: Lista de objetos `Message` que cumplen con los criterios de búsqueda.
        """
        return self.repository.get_by_session(session_id, limit, offset, sender)