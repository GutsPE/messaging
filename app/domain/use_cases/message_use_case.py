from abc import ABC, abstractmethod

class MessageUseCase(ABC):
    """
    Interfaz base para todos los casos de uso relacionados con mensajes.
    Define un método abstracto `execute` que debe ser implementado por cada caso de uso específico.
    """
    
    @abstractmethod
    def execute(self, *args, **kwargs):
        """
        Ejecuta la lógica principal del caso de uso.

        Args:
            *args: Argumentos posicionales variables.
            **kwargs: Argumentos con nombre variables.

        Returns:
            Cualquier tipo de resultado que defina el caso de uso implementado.
        """
        pass