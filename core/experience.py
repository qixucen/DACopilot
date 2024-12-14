# core/experience.py
from dataclasses import dataclass, field
from typing import Dict, List, Optional
import numpy as np

@dataclass
class Experience:
    """
    Represents a single experience entry containing question and function pairs
    """
    question: str
    function: str
    embedding: Optional[List[float]] = None
    cluster_id: Optional[int] = None
    metadata: Dict = field(default_factory=dict)

    def to_dict(self) -> Dict:
        """Convert experience to dictionary format"""
        return {
            "question": self.question,
            "function": self.function,
            "embedding": self.embedding,
            "cluster_id": self.cluster_id,
            "metadata": self.metadata
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Experience':
        """Create experience from dictionary format"""
        return cls(
            question=data["question"],
            function=data["function"],
            embedding=data.get("embedding"),
            cluster_id=data.get("cluster_id"),
            metadata=data.get("metadata", {})
        )

    def get_embedding_array(self) -> Optional[np.ndarray]:
        """Get embedding as numpy array"""
        if self.embedding is None:
            return None
        return np.array(self.embedding)