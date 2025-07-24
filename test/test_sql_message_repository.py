import pytest
from unittest.mock import MagicMock
from datetime import datetime, timezone

from app.infrastructure.repositories.sql_message_repository import SQLMessageRepository
from app.domain.entities.message import Message


@pytest.fixture
def fake_session():
    return MagicMock()


@pytest.fixture
def sample_message_model():
    mock_message = MagicMock()
    mock_message.id = 1
    mock_message.message_id = "msg-123"
    mock_message.session_id = "sess-001"
    mock_message.content = "Hello World"
    mock_message.timestamp = datetime.now(timezone.utc)
    mock_message.sender = "user"
    mock_message.length = 11
    mock_message.word_count = 2
    return mock_message


def test_get_all_returns_all_messages(fake_session, sample_message_model):
    fake_session.query().all.return_value = [sample_message_model]

    repo = SQLMessageRepository(fake_session)
    results = repo.get_all()

    assert len(results) == 1
    assert isinstance(results[0], Message)
    assert results[0].message_id == "msg-123"


def test_get_by_id_returns_message_when_found(fake_session, sample_message_model):
    fake_session.query().filter().first.return_value = sample_message_model

    repo = SQLMessageRepository(fake_session)
    result = repo.get_by_id("msg-123")

    assert isinstance(result, Message)
    assert result.session_id == "sess-001"


def test_get_by_id_returns_none_when_not_found(fake_session):
    fake_session.query().filter().first.return_value = None

    repo = SQLMessageRepository(fake_session)
    result = repo.get_by_id("non-existent")

    assert result is None


def test_save_persists_and_returns_message(fake_session, sample_message_model):
    # Simula commit y asignación de ID
    def add_side_effect(obj):
        obj.id = 1
        return obj

    fake_session.add.side_effect = add_side_effect
    fake_session.commit = MagicMock()

    repo = SQLMessageRepository(fake_session)

    domain_message = Message(
        id=None,
        message_id="msg-123",
        session_id="sess-001",
        content="Hello World",
        timestamp=sample_message_model.timestamp,
        sender="user",
        length=11,
        word_count=2
    )

    saved_message = repo.save(domain_message)

    assert isinstance(saved_message, Message)
    assert saved_message.id == 1
    assert saved_message.length == 11


def test_get_by_session_returns_filtered_messages(fake_session, sample_message_model):
    fake_session.query().filter().filter().offset().limit().all.return_value = [sample_message_model]

    repo = SQLMessageRepository(fake_session)
    results = repo.get_by_session("sess-001", limit=5, offset=0, sender="user")

    assert isinstance(results, list)
    assert len(results) == 1
    assert results[0].session_id == "sess-001"
    assert results[0].sender == "user"