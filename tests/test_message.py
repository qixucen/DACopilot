# tests/test_message.py
from datetime import datetime
from core.message import Message

def test_message_creation():
    message = Message("sender", "recipient", "content")
    assert message.sender_id == "sender"
    assert message.recipient_id == "recipient"
    assert message.content == "content"
    assert isinstance(message.timestamp, datetime)

def test_message_str():
    message = Message("sender", "recipient", "test content")
    expected = "Message from sender to recipient: test content"
    assert str(message) == expected