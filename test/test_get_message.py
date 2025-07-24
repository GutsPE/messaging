import pytest
from unittest.mock import MagicMock
from datetime import datetime, timezone

from app.domain.entities.message import Message
from app.application.services.get_message import GetMessage
from app.domain.exceptions.message_exceptions import MessageNotFoundException


@pytest.fixture
def mock_repository():
    return MagicMock()


@pytest.fixture
def use_case(mock_repository):
    return GetMessage(repository=mock_repository)


def test_execute_returns_message_when_found(use_case, mock_repository):
    # Arrange
    message_id = "msg-123"
    timestamp = datetime.now(timezone.utc)
    expected_message = Message(
        id=1,
        message_id=message_id,
        session_id="sess-123",
        content="Hola mundo",
        timestamp=timestamp,
        sender="user",
        length=10,
        word_count=2
    )
    mock_repository.get_by_id.return_value = expected_message

    # Act
    result = use_case.execute(message_id)

    # Assert
    mock_repository.get_by_id.assert_called_once_with(message_id)
    assert result == expected_message


def test_execute_raises_exception_when_message_not_found(use_case, mock_repository):
    # Arrange
    message_id = "non-existent"
    mock_repository.get_by_id.return_value = None

    # Act & Assert
    with pytest.raises(MessageNotFoundException) as exc_info:
        use_case.execute(message_id)

    assert str(exc_info.value) == f"Message with ID {message_id} not found."
    mock_repository.get_by_id.assert_called_once_with(message_id)
