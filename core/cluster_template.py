# core/cluster_template.py
from dataclasses import dataclass
from typing import List
from .experience import Experience

@dataclass
class ClusterTemplate:
    """
    Represents a generalized template for a cluster of similar experiences
    """
    question_template: str
    function_template: str
    examples: List[Experience]

    def to_dict(self):
        """Convert template to dictionary format"""
        return {
            "question_template": self.question_template,
            "function_template": self.function_template,
            "examples": [exp.to_dict() for exp in self.examples]
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'ClusterTemplate':
        """Create template from dictionary format"""
        return cls(
            question_template=data["question_template"],
            function_template=data["function_template"],
            examples=[Experience.from_dict(exp) for exp in data["examples"]]
        )