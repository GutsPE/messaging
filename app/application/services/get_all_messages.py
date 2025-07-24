from app.domain.repositories.message_repository import MessageRepository

class GetAllMessages:
    """
    Caso de uso para obtener todos los mensajes almacenados,
    sin aplicar filtros ni paginación.
    """
    def __init__(self, repository: MessageRepository):
        """
        Inicializa la clase con una instancia del repositorio de mensajes.

        Args:
            repository (MessageRepository): Repositorio que gestiona el acceso a los datos de mensajes.
        """
        self.repository = repository

    def execute(self):
        """
        Ejecuta la lógica para recuperar todos los mensajes disponibles en el repositorio.

        Returns:
            list[Message]: Lista completa de objetos `Message`.
        """
        return self.repository.get_all()