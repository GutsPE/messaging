import pytest
from unittest.mock import MagicMock
from datetime import datetime, timezone

from app.domain.entities.message import Message
from app.application.services.create_message import CreateMessage


@pytest.fixture
def mock_repository():
    return MagicMock()


@pytest.fixture
def create_message_use_case(mock_repository):
    return CreateMessage(repository=mock_repository)


def test_execute_creates_and_saves_message(create_message_use_case, mock_repository):
    # Datos de entrada
    message_id = "msg-001"
    session_id = "sess-123"
    content = "Hello there world"
    timestamp = datetime.now(timezone.utc)
    sender = "user"

    # Valor que debería devolver el repositorio al guardar
    expected_message = Message(
        id=1,
        message_id=message_id,
        session_id=session_id,
        content=content,
        timestamp=timestamp,
        sender=sender,
        length=len(content),
        word_count=len(content.split())
    )
    mock_repository.save.return_value = expected_message

    # Ejecutar el caso de uso
    result = create_message_use_case.execute(
        message_id=message_id,
        session_id=session_id,
        content=content,
        timestamp=timestamp,
        sender=sender
    )

    # Verificar que el método save fue llamado con una instancia de Message
    assert mock_repository.save.called
    saved_message = mock_repository.save.call_args[0][0]

    assert isinstance(saved_message, Message)
    assert saved_message.message_id == message_id
    assert saved_message.length == len(content)
    assert saved_message.word_count == len(content.split())

    # Verificar que el resultado final es el esperado
    assert result == expected_message