import pytest
from fastapi.testclient import TestClient
from app.main import app  # Asegúrate de importar la instancia de FastAPI
from datetime import datetime, timezone

# Cliente de pruebas
client = TestClient(app)


def test_get_all_messages(monkeypatch):
    # Mock de respuesta
    def mock_get_all(self):
        from app.domain.entities.message import Message
        return [
            Message(
                id=1,
                message_id="msg-123",
                session_id="sess-001",
                content="Hello",
                timestamp=datetime.now(timezone.utc),
                sender="user",
                length=5,
                word_count=1
            )
        ]

    from app.infrastructure.repositories.sql_message_repository import SQLMessageRepository
    monkeypatch.setattr(SQLMessageRepository, "get_all", mock_get_all)

    response = client.get("/messages/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert response.json()[0]["message_id"] == "msg-123"


def test_create_message(monkeypatch):
    payload = {
        "message_id": "msg-456",
        "session_id": "sess-002",
        "content": "Hola mundo",
        "timestamp": datetime.utcnow().isoformat(),
        "sender": "user"
    }

    def mock_execute(self, message_id, session_id, content, timestamp, sender):
        from app.domain.entities.message import Message
        return Message(
            id=1,
            message_id=message_id,
            session_id=session_id,
            content=content,
            timestamp=timestamp,
            sender=sender,
            length=len(content),
            word_count=len(content.split())
        )

    from app.application.services.create_message import CreateMessage
    monkeypatch.setattr(CreateMessage, "execute", mock_execute)

    response = client.post("/messages/", json=payload)
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert response.json()["data"]["message_id"] == "msg-456"


def test_get_message_by_id(monkeypatch):
    def mock_execute(self, message_id):
        from app.domain.entities.message import Message
        return Message(
            id=1,
            message_id=message_id,
            session_id="sess-001",
            content="Test message",
            timestamp=datetime.utcnow(),
            sender="user",
            length=12,
            word_count=2
        )

    from app.application.services.get_message import GetMessage
    monkeypatch.setattr(GetMessage, "execute", mock_execute)

    response = client.get("/messages/msg-001")
    assert response.status_code == 200
    assert response.json()["message_id"] == "msg-001"
    
    
def test_get_messages_by_session(monkeypatch):
    def mock_execute(self, session_id, limit=10, offset=0, sender=None):
        from app.domain.entities.message import Message
        return [
            Message(
                id=1,
                message_id="msg-789",
                session_id=session_id,
                content="Mensaje de prueba",
                timestamp=datetime.utcnow(),
                sender="system",
                length=17,
                word_count=3
            )
        ]

    from app.application.services.get_all_messages_by_session import GetAllMessagesBySession
    monkeypatch.setattr(GetAllMessagesBySession, "execute", mock_execute)

    response = client.get("/messages/sessions/sess-123?limit=5&offset=0&sender=system")
    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, list)
    assert body[0]["session_id"] == "sess-123"
    assert body[0]["sender"] == "system"