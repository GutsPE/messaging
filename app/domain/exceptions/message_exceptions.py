
class MessageNotFoundException(Exception):
    """
    Excepción personalizada que se lanza cuando un mensaje no se encuentra en la base de datos.

    Attributes:
        message (str): Mensaje de error que describe la excepción.
    """
    
    def __init__(self, message="Message not found"):
        """
        Inicializa la excepción con un mensaje personalizado.

        Args:
            message (str): Mensaje de error (por defecto "Message not found").
        """
        super().__init__(message)