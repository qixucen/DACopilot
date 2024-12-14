# core/message.py
from dataclasses import dataclass
from datetime import datetime
from typing import Any

@dataclass
class Message:
    sender_id: str
    recipient_id: str
    content: Any
    timestamp: datetime = datetime.now()
    
    def __str__(self):
        return f"Message from {self.sender_id} to {self.recipient_id}: {self.content}"