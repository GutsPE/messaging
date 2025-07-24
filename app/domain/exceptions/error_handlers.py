from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

async def custom_validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Manejador personalizado para errores de validación en FastAPI.

    Este manejador intercepta errores generados por validaciones de Pydantic (por ejemplo, tipo incorrecto o valor inválido).
    Si el error está relacionado con el campo 'sender' y su valor no es uno de los literales permitidos,
    retorna una respuesta personalizada con un mensaje específico.

    Args:
        request (Request): La solicitud que causó el error.
        exc (RequestValidationError): La excepción lanzada por FastAPI.

    Returns:
        JSONResponse: Respuesta JSON con el detalle del error.
    """
    errors = exc.errors() # Lista de errores encontrados en la validación

    # Recorremos los errores para buscar uno específico en el campo 'sender'
    for error in errors:
        if "sender" in str(error["loc"]) and error["type"] == "literal_error":
            return JSONResponse(
                status_code=422,
                content={
                    "status": "error",
                    "error": {
                        "code": "INVALID_FORMAT",
                        "message": "Formato de mensaje inválido",
                        "details": "El campo 'sender' debe ser 'user' o 'system'"
                    }
                }
            )

    # Si no es el caso del sender, devolvemos los errores estándar de validación
    return JSONResponse(
        status_code=422,
        content={
            "status": "error",
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Error de validación en la solicitud",
                "details": errors
            }
        }
    )