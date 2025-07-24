import pytest
from unittest.mock import MagicMock
from datetime import datetime, timezone

from app.domain.entities.message import Message
from app.application.services.get_all_messages_by_session import GetAllMessagesBySession


@pytest.fixture
def mock_repository():
    return MagicMock()


@pytest.fixture
def use_case(mock_repository):
    return GetAllMessagesBySession(repository=mock_repository)


def test_execute_returns_messages_for_session(use_case, mock_repository):
    # Datos simulados
    session_id = "sess-123"
    limit = 5
    offset = 0
    sender = "user"
    timestamp = datetime.now(timezone.utc)

    expected_messages = [
        Message(
            id=1,
            message_id="msg-1",
            session_id=session_id,
            content="Hola mundo",
            timestamp=timestamp,
            sender=sender,
            length=10,
            word_count=2
        ),
        Message(
            id=2,
            message_id="msg-2",
            session_id=session_id,
            content="Segundo mensaje",
            timestamp=timestamp,
            sender=sender,
            length=15,
            word_count=2
        ),
    ]

    # Simular retorno del repositorio
    mock_repository.get_by_session.return_value = expected_messages

    # Ejecutar el caso de uso
    result = use_case.execute(session_id, limit=limit, offset=offset, sender=sender)

    # Verificaciones
    mock_repository.get_by_session.assert_called_once_with(session_id, limit, offset, sender)
    assert result == expected_messages
