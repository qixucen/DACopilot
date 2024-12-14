# core/base_agent.py
import abc
from typing import List, Optional
from core.message import Message
from core.task import Task

class BaseAgent(abc.ABC):
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.messages: List[Message] = []
        
    @abc.abstractmethod
    def process(self, message: Message) -> Optional[Message]:
        """Process incoming message and generate response"""
        pass
    
    def receive_message(self, message: Message):
        """Receive and store message"""
        self.messages.append(message)
        
    def send_message(self, content: str, recipient_id: str) -> Message:
        """Create and send a new message"""
        message = Message(
            sender_id=self.agent_id,
            recipient_id=recipient_id,
            content=content
        )
        return message