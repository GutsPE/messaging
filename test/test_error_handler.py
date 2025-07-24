import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from fastapi.exceptions import RequestValidationError
from fastapi.requests import Request
from app.domain.exceptions.error_handlers import custom_validation_exception_handler
from app.infrastructure.handlers.message_handler import message_router

app = FastAPI()

# Registramos el manejador personalizado
app.add_exception_handler(RequestValidationError, custom_validation_exception_handler)

# Incluye tus rutas reales
app.include_router(message_router)

client = TestClient(app)


def test_invalid_sender_field():
    payload = {
        "message_id": "msg-001",
        "session_id": "sess-001",
        "content": "Hello, world!",
        "timestamp": "2025-07-24T12:34:56",
        "sender": "admin" 
    }

    response = client.post("/messages", json=payload)

    assert response.status_code == 422
    body = response.json()

    assert body["status"] == "error"
    assert body["error"]["code"] == "INVALID_FORMAT"
    assert "sender" in body["error"]["details"]


def test_missing_required_field():
    payload = {
        "message_id": "msg-002",
        "content": "Missing session_id",
        "timestamp": "2025-07-24T12:34:56",
        "sender": "user"
    }

    response = client.post("/messages", json=payload)

    assert response.status_code == 422
    body = response.json()

    assert body["status"] == "error"
    assert body["error"]["code"] == "VALIDATION_ERROR"
    assert any("session_id" in str(error["loc"]) for error in body["error"]["details"])
