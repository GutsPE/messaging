import pytest
import uuid
from datetime import datetime, timezone
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.infrastructure.handlers.message_handler import message_router
from app.domain.exceptions.error_handlers import custom_validation_exception_handler
from fastapi.exceptions import RequestValidationError


def create_test_app():
    app = FastAPI()
    app.include_router(message_router)
    app.add_exception_handler(RequestValidationError, custom_validation_exception_handler)
    return app


app = create_test_app()
client = TestClient(app)

@pytest.fixture
def sample_message():
    return {
        "message_id": str(uuid.uuid4()),
        "session_id": str(uuid.uuid4()),
        "content": "Hola mundo desde la prueba",
        "timestamp": datetime.utcnow().isoformat(),
        "sender": "user"
    }


def test_create_message_success():
    random_message_id = f"msg-{uuid.uuid4()}"
    payload = {
        "message_id": random_message_id,
        "session_id": "sess-001",
        "content": "Hola mundo",
        "timestamp": "2025-07-24T12:00:00",
        "sender": "user"
    }

    response = client.post("/messages", json=payload)

    assert response.status_code == 200
    body = response.json()

    assert body["status"] == "success"
    assert body["data"]["message_id"] == payload["message_id"]
    assert body["data"]["session_id"] == payload["session_id"]
    assert body["data"]["content"] == payload["content"]
    assert body["data"]["sender"] == payload["sender"]

    metadata = body["data"]["metadata"]
    assert metadata["word_count"] == 2
    assert metadata["character_count"] == len(payload["content"])

def test_create_message_invalid_sender():
    payload = {
        "message_id": "msg-003",
        "session_id": "sess-002",
        "content": "Mensaje inválido",
        "timestamp": "2025-07-24T12:10:00",
        "sender": "admin" 
    }

    response = client.post("/messages", json=payload)

    assert response.status_code == 422
    body = response.json()

    assert body["status"] == "error"
    assert body["error"]["code"] == "INVALID_FORMAT"
    assert "sender" in body["error"]["details"]
    
def test_create_message_missing_required_field():
    payload = {
        "message_id": "msg-004",
        # "session_id": "sess-003", 
        "content": "Falta session_id",
        "timestamp": "2025-07-24T12:20:00",
        "sender": "system"
    }

    response = client.post("/messages", json=payload)

    assert response.status_code == 422
    body = response.json()

    assert body["status"] == "error"
    assert body["error"]["code"] == "VALIDATION_ERROR"
    assert any("session_id" in str(e["loc"]) for e in body["error"]["details"])
    
def test_get_all_messages(sample_message):
    # Primero creamos un mensaje para que haya algo que recuperar
    client.post("/messages", json=sample_message)
    
    response = client.get("/messages")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert any(m["message_id"] == sample_message["message_id"] for m in response.json())

def test_get_message_by_id(sample_message):
    # Creamos el mensaje
    client.post("/messages", json=sample_message)

    # Lo recuperamos por ID
    response = client.get(f"/messages/{sample_message['message_id']}")
    assert response.status_code == 200
    assert response.json()["message_id"] == sample_message["message_id"]

def test_get_message_by_id_not_found():
    non_existent_id = str(uuid.uuid4())
    response = client.get(f"/messages/{non_existent_id}")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()

def test_get_messages_by_session(sample_message):
    # Creamos el mensaje
    client.post("/messages", json=sample_message)

    # Lo recuperamos por session_id
    response = client.get(f"/messages/sessions/{sample_message['session_id']}")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert any(m["message_id"] == sample_message["message_id"] for m in response.json())