import os
import json

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded
from dotenv import load_dotenv, find_dotenv
from fastapi import Request
from fastapi.responses import JSONResponse

from app.infrastructure.security.limiting import limiter
from app.infrastructure.handlers.message_handler import message_router
from app.infrastructure.handlers.realtime_handler import realtime_router

from app.domain.exceptions.error_handlers import custom_validation_exception_handler

load_dotenv(find_dotenv())

def app_constructor():
    app = FastAPI(
        title="API NAME", #  -> str Titulo de la API
        description="description", # -> str Descripcion de la API
        version="1.0.0", # -> str Version de la API
        contact={
            "name": "authors name",
            "email": "tuly.via@gmail.com"
        } # -> dict Informacion de contacto
    )

    app.add_middleware( # Validar CORS
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    routers = (
        message_router,
        realtime_router
    )

    # app.include_router(routers)

    for router in routers:
        app.include_router(router)
        
    # Configura rate limiter
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, lambda r, e: JSONResponse(
        status_code=429,
        content={"detail": "Rate limit exceeded"}
    ))
    app.add_middleware(SlowAPIMiddleware)
    
    # Registra el manejador de errores personalizado
    app.add_exception_handler(RequestValidationError, custom_validation_exception_handler)

    return app
