import pytest
from unittest.mock import MagicMock
from datetime import datetime, timezone

from app.domain.entities.message import Message
from app.application.services.get_all_messages import GetAllMessages


@pytest.fixture
def mock_repository():
    return MagicMock()


@pytest.fixture
def use_case(mock_repository):
    return GetAllMessages(repository=mock_repository)


def test_execute_returns_all_messages(use_case, mock_repository):
    # Datos simulados
    timestamp = datetime.now(timezone.utc)
    expected_messages = [
        Message(
            id=1,
            message_id="msg-1",
            session_id="sess-1",
            content="Hola mundo",
            timestamp=timestamp,
            sender="user",
            length=10,
            word_count=2
        ),
        Message(
            id=2,
            message_id="msg-2",
            session_id="sess-2",
            content="Segundo mensaje",
            timestamp=timestamp,
            sender="system",
            length=15,
            word_count=2
        ),
    ]

    mock_repository.get_all.return_value = expected_messages

    # Ejecutar el caso de uso
    result = use_case.execute()

    # Verificaciones
    mock_repository.get_all.assert_called_once()
    assert result == expected_messages
