from app.domain.repositories.message_repository import MessageRepository
from app.domain.exceptions.message_exceptions import MessageNotFoundException


class GetMessage:
    """
    Caso de uso para obtener un mensaje específico por su identificador único.
    """
    def __init__(self, repository: MessageRepository):
        """
        Inicializa la clase con un repositorio de mensajes.

        Args:
            repository (MessageRepository): Repositorio encargado del acceso a datos de mensajes.
        """
        self.repository = repository

    def execute(self, message_id: str):
        """
        Ejecuta la búsqueda de un mensaje a partir de su ID.

        Args:
            message_id (str): Identificador único del mensaje.

        Returns:
            Message: Objeto `Message` correspondiente al ID proporcionado.

        Raises:
            MessageNotFoundException: Si no se encuentra ningún mensaje con el ID dado.
        """
        message = self.repository.get_by_id(message_id)
        if not message:
            raise MessageNotFoundException(f"Message with ID {message_id} not found.")
        return message