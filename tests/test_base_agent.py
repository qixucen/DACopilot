# tests/test_base_agent.py
import pytest
from core.base_agent import BaseAgent
from core.message import Message

class TestAgent(BaseAgent):
    """Concrete implementation of BaseAgent for testing"""
    def process(self, message):
        return self.send_message("processed", "test_recipient")

def test_base_agent_initialization():
    agent = TestAgent("test_agent")
    assert agent.agent_id == "test_agent"
    assert agent.messages == []

def test_receive_message():
    agent = TestAgent("test_agent")
    message = Message("sender", "test_agent", "test content")
    agent.receive_message(message)
    assert len(agent.messages) == 1
    assert agent.messages[0] == message

def test_send_message():
    agent = TestAgent("test_agent")
    message = agent.send_message("test content", "recipient")
    assert message.sender_id == "test_agent"
    assert message.recipient_id == "recipient"
    assert message.content == "test content"

def test_process_message():
    agent = TestAgent("test_agent")
    input_message = Message("sender", "test_agent", "test content")
    response = agent.process(input_message)
    assert response.sender_id == "test_agent"
    assert response.recipient_id == "test_recipient"
    assert response.content == "processed"